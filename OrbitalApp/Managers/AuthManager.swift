import Foundation
import SwiftUI

@MainActor
class AuthManager: ObservableObject {
    @Published var isAuthenticated = false
    @Published var isLoading = false
    @Published var userEmail = ""
    @Published var minutesBalance: Double = 0
    @Published var memberSince = ""
    
    private let supabaseURL = "https://pqwhfiuvcsjfevjwljml.supabase.co"
    private let supabaseAnonKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBxd2hmaXV2Y3NqZmV2andsam1sIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA3ODUwNzIsImV4cCI6MjA4NjM2MTA3Mn0.aKjsKhSDwJLaPknRct37eoQl5SFVo7S528yS9inJB-A"
    
    @AppStorage("accessToken") private var accessToken: String = ""
    @AppStorage("refreshToken") private var refreshToken: String = ""
    
    init() {
        // Check if we have a stored session
        if !accessToken.isEmpty {
            Task {
                await validateSession()
            }
        }
    }
    
    // MARK: - Sign In
    func signIn(email: String, password: String) async throws {
        isLoading = true
        defer { isLoading = false }
        
        let url = URL(string: "\(supabaseURL)/auth/v1/token?grant_type=password")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue(supabaseAnonKey, forHTTPHeaderField: "apikey")
        
        let body = ["email": email, "password": password]
        request.httpBody = try JSONEncoder().encode(body)
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw AuthError.invalidResponse
        }
        
        if httpResponse.statusCode != 200 {
            let errorResponse = try? JSONDecoder().decode(AuthErrorResponse.self, from: data)
            throw AuthError.serverError(errorResponse?.errorDescription ?? "Login failed")
        }
        
        let authResponse = try JSONDecoder().decode(AuthResponse.self, from: data)
        
        // Store tokens
        accessToken = authResponse.accessToken
        refreshToken = authResponse.refreshToken
        
        // Update state
        userEmail = authResponse.user.email ?? ""
        isAuthenticated = true
        
        // Fetch profile
        await fetchProfile()
    }
    
    // MARK: - Sign Up
    func signUp(email: String, password: String) async throws {
        isLoading = true
        defer { isLoading = false }
        
        let url = URL(string: "\(supabaseURL)/auth/v1/signup")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue(supabaseAnonKey, forHTTPHeaderField: "apikey")
        
        let body = ["email": email, "password": password]
        request.httpBody = try JSONEncoder().encode(body)
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw AuthError.invalidResponse
        }
        
        if httpResponse.statusCode != 200 && httpResponse.statusCode != 201 {
            let errorResponse = try? JSONDecoder().decode(AuthErrorResponse.self, from: data)
            throw AuthError.serverError(errorResponse?.errorDescription ?? "Signup failed")
        }
        
        // Note: User needs to verify email before signing in
    }
    
    // MARK: - Sign Out
    func signOut() {
        accessToken = ""
        refreshToken = ""
        userEmail = ""
        minutesBalance = 0
        isAuthenticated = false
    }
    
    // MARK: - Validate Session
    func validateSession() async {
        guard !accessToken.isEmpty else { return }
        
        let url = URL(string: "\(supabaseURL)/auth/v1/user")!
        var request = URLRequest(url: url)
        request.setValue("Bearer \(accessToken)", forHTTPHeaderField: "Authorization")
        request.setValue(supabaseAnonKey, forHTTPHeaderField: "apikey")
        
        do {
            let (data, response) = try await URLSession.shared.data(for: request)
            
            guard let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 else {
                // Token invalid, try refresh
                await refreshSession()
                return
            }
            
            let user = try JSONDecoder().decode(User.self, from: data)
            userEmail = user.email ?? ""
            isAuthenticated = true
            
            await fetchProfile()
        } catch {
            signOut()
        }
    }
    
    // MARK: - Refresh Session
    func refreshSession() async {
        guard !refreshToken.isEmpty else {
            signOut()
            return
        }
        
        let url = URL(string: "\(supabaseURL)/auth/v1/token?grant_type=refresh_token")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue(supabaseAnonKey, forHTTPHeaderField: "apikey")
        
        let body = ["refresh_token": refreshToken]
        request.httpBody = try? JSONEncoder().encode(body)
        
        do {
            let (data, response) = try await URLSession.shared.data(for: request)
            
            guard let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 else {
                signOut()
                return
            }
            
            let authResponse = try JSONDecoder().decode(AuthResponse.self, from: data)
            accessToken = authResponse.accessToken
            refreshToken = authResponse.refreshToken
            userEmail = authResponse.user.email ?? ""
            isAuthenticated = true
            
            await fetchProfile()
        } catch {
            signOut()
        }
    }
    
    // MARK: - Fetch Profile
    func fetchProfile() async {
        let url = URL(string: "\(supabaseURL)/rest/v1/profiles?select=*&limit=1")!
        var request = URLRequest(url: url)
        request.setValue("Bearer \(accessToken)", forHTTPHeaderField: "Authorization")
        request.setValue(supabaseAnonKey, forHTTPHeaderField: "apikey")
        
        do {
            let (data, _) = try await URLSession.shared.data(for: request)
            let profiles = try JSONDecoder().decode([Profile].self, from: data)
            
            if let profile = profiles.first {
                minutesBalance = profile.minutesBalance
                
                let formatter = DateFormatter()
                formatter.dateFormat = "yyyy-MM-dd"
                if let date = formatter.date(from: String(profile.createdAt.prefix(10))) {
                    let displayFormatter = DateFormatter()
                    displayFormatter.dateFormat = "MMM yyyy"
                    memberSince = displayFormatter.string(from: date)
                }
            }
        } catch {
            print("Failed to fetch profile: \(error)")
        }
    }
}

// MARK: - Models
struct AuthResponse: Codable {
    let accessToken: String
    let refreshToken: String
    let user: User
    
    enum CodingKeys: String, CodingKey {
        case accessToken = "access_token"
        case refreshToken = "refresh_token"
        case user
    }
}

struct User: Codable {
    let id: String
    let email: String?
}

struct Profile: Codable {
    let id: String
    let email: String
    let minutesBalance: Double
    let createdAt: String
    
    enum CodingKeys: String, CodingKey {
        case id
        case email
        case minutesBalance = "minutes_balance"
        case createdAt = "created_at"
    }
}

struct AuthErrorResponse: Codable {
    let error: String?
    let errorDescription: String?
    
    enum CodingKeys: String, CodingKey {
        case error
        case errorDescription = "error_description"
    }
}

enum AuthError: LocalizedError {
    case invalidResponse
    case serverError(String)
    
    var errorDescription: String? {
        switch self {
        case .invalidResponse: return "Invalid server response"
        case .serverError(let message): return message
        }
    }
}
