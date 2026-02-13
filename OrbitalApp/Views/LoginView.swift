import SwiftUI

struct LoginView: View {
    @EnvironmentObject var authManager: AuthManager
    
    @State private var email = ""
    @State private var password = ""
    @State private var isSignUp = false
    @State private var errorMessage: String?
    @State private var showingError = false
    @State private var showingSuccess = false
    @FocusState private var focusedField: Field?
    
    enum Field {
        case email, password
    }
    
    var body: some View {
        ScrollView {
            VStack(spacing: 32) {
                // Logo
                OrbitalLogo()
                    .frame(height: 120)
                    .padding(.top, 60)
                
                // Title
                VStack(spacing: 8) {
                    Text(isSignUp ? "Create Account" : "Welcome back")
                        .font(.title)
                        .fontWeight(.bold)
                        .foregroundStyle(.white)
                    
                    Text(isSignUp ? "Start solving problems today" : "Sign in to continue solving")
                        .font(.subheadline)
                        .foregroundStyle(OrbitalColors.textSecondaryDark)
                }
                
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
                                        .foregroundColor(OrbitalColors.dimWhite)
                                }
                                TextField("", text: $email)
                                    .textContentType(.emailAddress)
                                    .keyboardType(.emailAddress)
                                    .autocapitalization(.none)
                                    .foregroundColor(.white)
                                    .tint(.white)
                                    .focused($focusedField, equals: .email)
                            }
                        }
                        .padding()
                        .neonInputStyle()
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
                                        .foregroundColor(OrbitalColors.dimWhite)
                                }
                                SecureField("", text: $password)
                                    .textContentType(isSignUp ? .newPassword : .password)
                                    .foregroundColor(.white)
                                    .tint(.white)
                                    .focused($focusedField, equals: .password)
                            }
                        }
                        .padding()
                        .neonInputStyle()
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
                
                // Sign In button - Metallic silver
                Button(action: submitForm) {
                    HStack {
                        if authManager.isLoading {
                            ProgressView()
                                .tint(.black)
                        }
                        Text(isSignUp ? "Create Account" : "Sign In")
                            .fontWeight(.semibold)
                    }
                    .frame(maxWidth: .infinity)
                    .padding()
                    .silverButtonStyle()
                }
                .disabled(email.isEmpty || password.isEmpty || authManager.isLoading)
                .opacity(email.isEmpty || password.isEmpty ? 0.6 : 1)
                .padding(.horizontal)
                
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
                .padding(.horizontal)
                
                // Google Sign In
                Button(action: signInWithGoogle) {
                    HStack {
                        Image(systemName: "g.circle.fill")
                            .font(.title3)
                        Text("Continue with Google")
                            .fontWeight(.medium)
                    }
                    .frame(maxWidth: .infinity)
                    .padding()
                    .outlineButtonStyle()
                }
                .padding(.horizontal)
                
                // Toggle sign up/sign in
                HStack {
                    Text(isSignUp ? "Already have an account?" : "Don't have an account?")
                        .foregroundStyle(OrbitalColors.textSecondaryDark)
                    
                    Button(isSignUp ? "Sign In" : "Sign Up") {
                        withAnimation {
                            isSignUp.toggle()
                        }
                    }
                    .foregroundColor(.white)
                    .fontWeight(.bold)
                }
                .font(.subheadline)
                
                Spacer(minLength: 50)
            }
        }
        .orbitalGradientBackground()
        .tint(.white) // Override app tint
        .onTapGesture {
            focusedField = nil
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
    
    func submitForm() {
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
        // TODO: Implement
    }
}

#Preview {
    LoginView()
        .environmentObject(AuthManager())
        .preferredColorScheme(.dark)
}
