//
//  LoginView.swift
//  Orbital - AI Math Video Solver
//
//  Premium login/signup screen with Tesla-level polish:
//    - Deep Space gradient background
//    - Breathing logo with purple aura animation
//    - Staggered entrance animations
//    - Focus-reactive input glow
//    - Shimmer effect on primary CTA
//    - Google OAuth button
//    - Haptic feedback throughout
//
//  Copyright © 2026 Onyx Enterprises. All rights reserved.
//

import SwiftUI

/// Login and signup view with premium animations and styling.
struct LoginView: View {
    @EnvironmentObject var authManager: AuthManager
    @ObservedObject var accentTheme = AccentTheme.shared
    
    @State private var email = ""
    @State private var password = ""
    @State private var isSignUp = false
    @State private var errorMessage: String?
    @State private var showingError = false
    @State private var showingSuccess = false
    @FocusState private var focusedField: Field?
    
    // Animation states
    @State private var logoOpacity = 0.0
    @State private var logoOffset: CGFloat = 20
    @State private var titleOpacity = 0.0
    @State private var titleOffset: CGFloat = 20
    @State private var formOpacity = 0.0
    @State private var formOffset: CGFloat = 20
    @State private var buttonsOpacity = 0.0
    @State private var buttonsOffset: CGFloat = 20
    @State private var shimmerOffset: CGFloat = -200
    
    enum Field {
        case email, password
    }
    
    var body: some View {
        ScrollView {
            VStack(spacing: 28) {
                // Logo with breathing glow + ORBITAL text
                VStack(spacing: 12) {
                    BreathingLogo()
                        .frame(height: 100)
                    
                    Text("ORBITAL")
                        .font(.system(size: 14, weight: .medium))
                        .tracking(6)
                        .foregroundStyle(OrbitalColors.dimWhite)
                }
                .padding(.top, 50)
                .opacity(logoOpacity)
                .offset(y: logoOffset)
                
                // Title
                VStack(spacing: 8) {
                    Text(isSignUp ? "Create Account" : "Welcome back")
                        .font(.system(size: 32, weight: .bold))
                        .foregroundStyle(.white)
                    
                    Text(isSignUp ? "Start solving problems today" : "Sign in to continue solving")
                        .font(.subheadline)
                        .foregroundStyle(OrbitalColors.textSecondaryDark)
                }
                .opacity(titleOpacity)
                .offset(y: titleOffset)
                
                // Form
                VStack(spacing: 20) {
                    // Email
                    VStack(alignment: .leading, spacing: 8) {
                        Text("EMAIL")
                            .font(.caption)
                            .fontWeight(.medium)
                            .foregroundStyle(OrbitalColors.textSecondaryDark)
                            .tracking(1.5)
                        
                        HStack {
                            Image(systemName: "envelope")
                                .foregroundColor(OrbitalColors.dimWhite)
                            
                            ZStack(alignment: .leading) {
                                if email.isEmpty {
                                    Text("you@example.com")
                                        .font(.system(size: 20))
                                        .foregroundColor(OrbitalColors.dimWhite)
                                }
                                TextField("", text: $email)
                                    .font(.system(size: 20))
                                    .textContentType(.emailAddress)
                                    .keyboardType(.emailAddress)
                                    .autocapitalization(.none)
                                    .foregroundColor(.white)
                                    .tint(.white)
                                    .focused($focusedField, equals: .email)
                            }
                        }
                        .padding()
                        .background(OrbitalColors.cardDark)
                        .clipShape(RoundedRectangle(cornerRadius: 12))
                        .overlay(
                            RoundedRectangle(cornerRadius: 12)
                                .stroke(OrbitalColors.accent.opacity(focusedField == .email ? 0.4 : 0.15), lineWidth: 1)
                        )
                        .shadow(color: OrbitalColors.accent.opacity(focusedField == .email ? 0.35 : 0.15), radius: focusedField == .email ? 15 : 8, x: 0, y: focusedField == .email ? 8 : 4)
                        .animation(.easeInOut(duration: 0.2), value: focusedField)
                    }
                    
                    // Password
                    VStack(alignment: .leading, spacing: 8) {
                        Text("PASSWORD")
                            .font(.caption)
                            .fontWeight(.medium)
                            .foregroundStyle(OrbitalColors.textSecondaryDark)
                            .tracking(1.5)
                        
                        HStack {
                            Image(systemName: "lock")
                                .foregroundColor(OrbitalColors.dimWhite)
                            
                            ZStack(alignment: .leading) {
                                if password.isEmpty {
                                    Text("••••••••")
                                        .font(.system(size: 20))
                                        .foregroundColor(OrbitalColors.dimWhite)
                                }
                                SecureField("", text: $password)
                                    .font(.system(size: 20))
                                    .textContentType(isSignUp ? .newPassword : .password)
                                    .foregroundColor(.white)
                                    .tint(.white)
                                    .focused($focusedField, equals: .password)
                            }
                        }
                        .padding()
                        .background(OrbitalColors.cardDark)
                        .clipShape(RoundedRectangle(cornerRadius: 12))
                        .overlay(
                            RoundedRectangle(cornerRadius: 12)
                                .stroke(OrbitalColors.accent.opacity(focusedField == .password ? 0.4 : 0.15), lineWidth: 1)
                        )
                        .shadow(color: OrbitalColors.accent.opacity(focusedField == .password ? 0.35 : 0.15), radius: focusedField == .password ? 15 : 8, x: 0, y: focusedField == .password ? 8 : 4)
                        .animation(.easeInOut(duration: 0.2), value: focusedField)
                    }
                    
                    if !isSignUp {
                        HStack {
                            Spacer()
                            Button("Forgot password?") {
                                // TODO: Implement
                            }
                            .font(.subheadline)
                            .foregroundColor(OrbitalColors.neonWhite)
                        }
                    }
                }
                .padding(.horizontal)
                .opacity(formOpacity)
                .offset(y: formOffset)
                
                // Buttons section
                VStack(spacing: 16) {
                    // Sign In button - Purple gradient primary CTA
                    Button(action: submitForm) {
                        HStack(spacing: 8) {
                            if authManager.isLoading {
                                ProgressView()
                                    .tint(.white)
                            }
                            Text(isSignUp ? "Create Account" : "Sign In")
                                .font(.system(size: 17, weight: .bold))
                                .tracking(0.5)
                        }
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 16)
                        .background(
                            ZStack {
                                // Purple gradient
                                LinearGradient(
                                    colors: [
                                        OrbitalColors.accentLight,
                                        OrbitalColors.accent,
                                    ],
                                    startPoint: .top,
                                    endPoint: .bottom
                                )
                                
                                // Shimmer
                                LinearGradient(
                                    colors: [.clear, .white.opacity(0.3), .clear],
                                    startPoint: .leading,
                                    endPoint: .trailing
                                )
                                .frame(width: 100)
                                .offset(x: shimmerOffset)
                                .blur(radius: 8)
                            }
                        )
                        .foregroundStyle(.white)
                        .clipShape(RoundedRectangle(cornerRadius: 12))
                        // Purple glow underneath
                        .shadow(color: OrbitalColors.accent.opacity(0.5), radius: 12, x: 0, y: 6)
                        .shadow(color: OrbitalColors.accent.opacity(0.3), radius: 20, x: 0, y: 10)
                    }
                    .disabled(email.isEmpty || password.isEmpty || authManager.isLoading)
                    .opacity(email.isEmpty || password.isEmpty ? 0.6 : 1)
                    .onAppear {
                        withAnimation(.linear(duration: 2.5).repeatForever(autoreverses: false)) {
                            shimmerOffset = 400
                        }
                    }
                    
                    // Divider
                    HStack {
                        Rectangle()
                            .fill(OrbitalColors.cardBorderDark)
                            .frame(height: 1)
                        Text("OR")
                            .font(.caption)
                            .foregroundStyle(OrbitalColors.textSecondaryDark)
                        Rectangle()
                            .fill(OrbitalColors.cardBorderDark)
                            .frame(height: 1)
                    }
                    
                    // Google Sign In with actual G logo
                    Button(action: signInWithGoogle) {
                        HStack(spacing: 12) {
                            Image("GoogleLogo")
                                .resizable()
                                .aspectRatio(contentMode: .fit)
                                .frame(width: 24, height: 24)
                                .shadow(color: OrbitalColors.accent.opacity(0.4), radius: 6, x: 0, y: 0)
                            
                            Text("Continue with Google")
                                .fontWeight(.medium)
                        }
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(OrbitalColors.cardDark)
                        .foregroundStyle(.white)
                        .clipShape(RoundedRectangle(cornerRadius: 12))
                        .overlay(
                            RoundedRectangle(cornerRadius: 12)
                                .stroke(Color.white.opacity(0.15), lineWidth: 1)
                        )
                    }
                    
                    // Toggle sign up/sign in
                    HStack {
                        Text(isSignUp ? "Already have an account?" : "Don't have an account?")
                            .foregroundStyle(OrbitalColors.textSecondaryDark)
                        
                        Button(isSignUp ? "Sign In" : "Sign Up") {
                            let generator = UIImpactFeedbackGenerator(style: .light)
                            generator.impactOccurred()
                            withAnimation {
                                isSignUp.toggle()
                            }
                        }
                        .foregroundColor(OrbitalColors.accent)
                        .fontWeight(.bold)
                    }
                    .font(.subheadline)
                }
                .padding(.horizontal)
                .opacity(buttonsOpacity)
                .offset(y: buttonsOffset)
                
                // Terms link at bottom
                Text("By signing in, you agree to our ")
                    .foregroundStyle(OrbitalColors.textSecondaryDark)
                +
                Text("Terms")
                    .foregroundStyle(OrbitalColors.dimWhite)
                +
                Text(" & ")
                    .foregroundStyle(OrbitalColors.textSecondaryDark)
                +
                Text("Privacy")
                    .foregroundStyle(OrbitalColors.dimWhite)
                
                Spacer(minLength: 30)
            }
            .font(.caption2)
        }
        .orbitalGradientBackground()
        .tint(.white)
        .onTapGesture {
            focusedField = nil
        }
        .onAppear {
            startEntranceAnimations()
        }
        .alert("Error", isPresented: $showingError) {
            Button("OK") { }
        } message: {
            Text(errorMessage ?? "An error occurred")
        }
        .alert("Check your email", isPresented: $showingSuccess) {
            Button("OK") { }
        } message: {
            Text("We sent you a confirmation link. Please check your email to verify your account.")
        }
    }
    
    func startEntranceAnimations() {
        withAnimation(.easeOut(duration: 0.6)) {
            logoOpacity = 1
            logoOffset = 0
        }
        
        withAnimation(.easeOut(duration: 0.6).delay(0.15)) {
            titleOpacity = 1
            titleOffset = 0
        }
        
        withAnimation(.easeOut(duration: 0.6).delay(0.3)) {
            formOpacity = 1
            formOffset = 0
        }
        
        withAnimation(.easeOut(duration: 0.6).delay(0.45)) {
            buttonsOpacity = 1
            buttonsOffset = 0
        }
    }
    
    func submitForm() {
        let generator = UIImpactFeedbackGenerator(style: .medium)
        generator.impactOccurred()
        
        Task {
            do {
                if isSignUp {
                    try await authManager.signUp(email: email, password: password)
                    showingSuccess = true
                } else {
                    try await authManager.signIn(email: email, password: password)
                }
            } catch {
                errorMessage = error.localizedDescription
                showingError = true
            }
        }
    }
    
    func signInWithGoogle() {
        let generator = UIImpactFeedbackGenerator(style: .light)
        generator.impactOccurred()
        // TODO: Implement
    }
}

// BreathingLogo is defined in Components/OrbitalLogo.swift

#Preview {
    LoginView()
        .environmentObject(AuthManager())
        .preferredColorScheme(.dark)
}
