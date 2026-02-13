//
//  ProfileView.swift
//  Orbital - AI Math Video Solver
//
//  User profile and settings screen. Features:
//    - Minutes balance with circular progress indicator
//    - "Manage Minutes" button (opens Safari to web checkout)
//    - Dark/Light mode toggle
//    - Settings sections (Preferences, Support, Legal)
//    - Sign out with confirmation
//
//  Note: Purchases happen on web to avoid Apple's 30% cut.
//  The "Manage Minutes" button passes the auth token to the website.
//
//  Copyright © 2026 Onyx Enterprises. All rights reserved.
//

import SwiftUI

/// User profile, settings, and minute balance management.
struct ProfileView: View {
    @Environment(\.colorScheme) var colorScheme
    @EnvironmentObject var authManager: AuthManager
    @AppStorage("isDarkMode") private var isDarkMode = true
    @State private var showingSignOutAlert = false
    
    // Animation states
    @State private var headerOpacity = 0.0
    @State private var headerOffset: CGFloat = 20
    @State private var contentOpacity = 0.0
    @State private var contentOffset: CGFloat = 20
    
    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 24) {
                    // Breathing logo
                    BreathingLogo()
                        .frame(height: 50)
                        .padding(.top, 10)
                        .opacity(headerOpacity)
                        .offset(y: headerOffset)
                    
                    // Profile header
                    VStack(spacing: 16) {
                        // Avatar
                        Circle()
                            .fill(
                                LinearGradient(
                                    colors: [OrbitalColors.accentLight, OrbitalColors.accent],
                                    startPoint: .topLeading,
                                    endPoint: .bottomTrailing
                                )
                            )
                            .frame(width: 80, height: 80)
                            .overlay(
                                Text(authManager.userEmail.prefix(1).uppercased())
                                    .font(.system(size: 32, weight: .bold))
                                    .foregroundStyle(.white)
                            )
                            .shadow(color: OrbitalColors.accent.opacity(0.4), radius: 12)
                        
                        VStack(spacing: 4) {
                            Text(authManager.userEmail)
                                .font(.headline)
                                .foregroundStyle(OrbitalColors.textPrimary(colorScheme))
                            
                            Text("Member since \(authManager.memberSince)")
                                .font(.caption)
                                .foregroundStyle(OrbitalColors.textSecondary(colorScheme))
                        }
                    }
                    .opacity(headerOpacity)
                    .offset(y: headerOffset)
                    
                    // Minutes balance card with purple glow
                    VStack(spacing: 16) {
                        HStack {
                            VStack(alignment: .leading, spacing: 4) {
                                Text("Minutes Left")
                                    .font(.subheadline)
                                    .foregroundStyle(OrbitalColors.textSecondary(colorScheme))
                                
                                HStack(alignment: .firstTextBaseline, spacing: 4) {
                                    Text("\(authManager.minutesBalance, specifier: "%.1f")")
                                        .font(.system(size: 42, weight: .bold))
                                        .foregroundStyle(OrbitalColors.textPrimary(colorScheme))
                                    Text("minutes")
                                        .font(.headline)
                                        .foregroundStyle(OrbitalColors.textSecondary(colorScheme))
                                }
                            }
                            
                            Spacer()
                            
                            // Circular indicator
                            ZStack {
                                Circle()
                                    .stroke(OrbitalColors.cardBorder(colorScheme), lineWidth: 6)
                                    .frame(width: 60, height: 60)
                                
                                Circle()
                                    .trim(from: 0, to: min(authManager.minutesBalance / 100, 1))
                                    .stroke(
                                        LinearGradient(
                                            colors: [OrbitalColors.accentLight, OrbitalColors.accent],
                                            startPoint: .topLeading,
                                            endPoint: .bottomTrailing
                                        ),
                                        style: StrokeStyle(lineWidth: 6, lineCap: .round)
                                    )
                                    .frame(width: 60, height: 60)
                                    .rotationEffect(.degrees(-90))
                                
                                if authManager.minutesBalance == 0 {
                                    Text("⛽")
                                        .font(.system(size: 20))
                                }
                            }
                        }
                        
                        // Manage Minutes button
                        Button(action: openManageMinutes) {
                            HStack {
                                Text("Manage Minutes")
                                    .font(.system(size: 16, weight: .semibold))
                                Spacer()
                                Image(systemName: "arrow.up.right")
                                    .font(.system(size: 14, weight: .semibold))
                            }
                            .padding()
                            .background(
                                LinearGradient(
                                    colors: [OrbitalColors.accentLight, OrbitalColors.accent],
                                    startPoint: .leading,
                                    endPoint: .trailing
                                )
                            )
                            .foregroundStyle(.white)
                            .clipShape(RoundedRectangle(cornerRadius: 12))
                            .shadow(color: OrbitalColors.accent.opacity(0.4), radius: 10, x: 0, y: 4)
                        }
                    }
                    .padding(20)
                    .background(OrbitalColors.card(colorScheme))
                    .clipShape(RoundedRectangle(cornerRadius: 20))
                    .overlay(
                        RoundedRectangle(cornerRadius: 20)
                            .stroke(OrbitalColors.accent.opacity(0.2), lineWidth: 1)
                    )
                    .shadow(color: OrbitalColors.accent.opacity(0.15), radius: 15, x: 0, y: 5)
                    .padding(.horizontal)
                    .opacity(contentOpacity)
                    .offset(y: contentOffset)
                    
                    // Settings sections
                    VStack(spacing: 12) {
                        // Preferences
                        ProfileSettingsSection(title: "Preferences", colorScheme: colorScheme) {
                            ProfileSettingsRow(
                                icon: "moon.fill",
                                title: "Dark Mode",
                                colorScheme: colorScheme,
                                trailing: {
                                    Toggle("", isOn: $isDarkMode)
                                        .tint(OrbitalColors.accent)
                                }
                            )
                            
                            ProfileSettingsRow(
                                icon: "bell.fill",
                                title: "Notifications",
                                colorScheme: colorScheme,
                                trailing: {
                                    Image(systemName: "chevron.right")
                                        .foregroundStyle(OrbitalColors.accent)
                                }
                            )
                        }
                        
                        // Support
                        ProfileSettingsSection(title: "Support", colorScheme: colorScheme) {
                            ProfileSettingsRow(
                                icon: "questionmark.circle.fill",
                                title: "Help Center",
                                colorScheme: colorScheme,
                                trailing: {
                                    Image(systemName: "arrow.up.right")
                                        .foregroundStyle(OrbitalColors.accent)
                                }
                            )
                            
                            ProfileSettingsRow(
                                icon: "envelope.fill",
                                title: "Contact Us",
                                colorScheme: colorScheme,
                                trailing: {
                                    Image(systemName: "arrow.up.right")
                                        .foregroundStyle(OrbitalColors.accent)
                                }
                            )
                        }
                        
                        // Legal
                        ProfileSettingsSection(title: "Legal", colorScheme: colorScheme) {
                            ProfileSettingsRow(
                                icon: "doc.text.fill",
                                title: "Terms of Service",
                                colorScheme: colorScheme,
                                trailing: {
                                    Image(systemName: "arrow.up.right")
                                        .foregroundStyle(OrbitalColors.accent)
                                }
                            )
                            
                            ProfileSettingsRow(
                                icon: "hand.raised.fill",
                                title: "Privacy Policy",
                                colorScheme: colorScheme,
                                trailing: {
                                    Image(systemName: "arrow.up.right")
                                        .foregroundStyle(OrbitalColors.accent)
                                }
                            )
                        }
                    }
                    .padding(.horizontal)
                    .opacity(contentOpacity)
                    .offset(y: contentOffset)
                    
                    // Sign out button
                    Button(action: { showingSignOutAlert = true }) {
                        HStack {
                            Image(systemName: "rectangle.portrait.and.arrow.right")
                            Text("Sign Out")
                        }
                        .font(.system(size: 16, weight: .medium))
                        .foregroundStyle(Color(red: 1, green: 0.4, blue: 0.4))
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(OrbitalColors.card(colorScheme))
                        .clipShape(RoundedRectangle(cornerRadius: 12))
                        .overlay(
                            RoundedRectangle(cornerRadius: 12)
                                .stroke(Color(red: 1, green: 0.4, blue: 0.4).opacity(0.2), lineWidth: 1)
                        )
                    }
                    .padding(.horizontal)
                    .opacity(contentOpacity)
                    .offset(y: contentOffset)
                    
                    Spacer(minLength: 50)
                }
            }
            .orbitalGradientBackground()
            .navigationTitle("Profile")
            .navigationBarTitleDisplayMode(.inline)
            .toolbarColorScheme(colorScheme, for: .navigationBar)
            .onAppear {
                startEntranceAnimations()
            }
            .alert("Sign Out", isPresented: $showingSignOutAlert) {
                Button("Cancel", role: .cancel) { }
                Button("Sign Out", role: .destructive) {
                    authManager.signOut()
                }
            } message: {
                Text("Are you sure you want to sign out?")
            }
        }
        .preferredColorScheme(isDarkMode ? .dark : .light)
    }
    
    func startEntranceAnimations() {
        withAnimation(.easeOut(duration: 0.5)) {
            headerOpacity = 1
            headerOffset = 0
        }
        
        withAnimation(.easeOut(duration: 0.5).delay(0.15)) {
            contentOpacity = 1
            contentOffset = 0
        }
    }
    
    func openManageMinutes() {
        let generator = UIImpactFeedbackGenerator(style: .medium)
        generator.impactOccurred()
        
        let baseURL = "https://orbitalsolver.io/account"
        let token = authManager.accessToken
        
        if let url = URL(string: "\(baseURL)?token=\(token)") {
            UIApplication.shared.open(url)
        }
    }
}

// MARK: - Settings Section
struct ProfileSettingsSection<Content: View>: View {
    let title: String
    let colorScheme: ColorScheme
    @ViewBuilder let content: Content
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(title.uppercased())
                .font(.caption)
                .fontWeight(.medium)
                .foregroundStyle(OrbitalColors.textSecondary(colorScheme))
                .tracking(1)
                .padding(.horizontal, 4)
            
            VStack(spacing: 0) {
                content
            }
            .background(OrbitalColors.card(colorScheme))
            .clipShape(RoundedRectangle(cornerRadius: 16))
            .overlay(
                RoundedRectangle(cornerRadius: 16)
                    .stroke(OrbitalColors.cardBorder(colorScheme), lineWidth: 1)
            )
        }
    }
}

// MARK: - Settings Row
struct ProfileSettingsRow<Trailing: View>: View {
    let icon: String
    let title: String
    let colorScheme: ColorScheme
    @ViewBuilder let trailing: Trailing
    
    var body: some View {
        HStack {
            Image(systemName: icon)
                .font(.system(size: 16))
                .foregroundStyle(OrbitalColors.accent)
                .frame(width: 28)
            
            Text(title)
                .font(.system(size: 16))
                .foregroundStyle(OrbitalColors.textPrimary(colorScheme))
            
            Spacer()
            
            trailing
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 14)
    }
}

#Preview {
    ProfileView()
        .environmentObject(AuthManager())
        .preferredColorScheme(.dark)
}
