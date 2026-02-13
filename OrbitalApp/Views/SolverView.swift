import SwiftUI

struct SolverView: View {
    @EnvironmentObject var authManager: AuthManager
    @State private var problemText = ""
    @State private var isGenerating = false
    @State private var showingImagePicker = false
    @FocusState private var isInputFocused: Bool
    
    let exampleProblems = [
        "Solve for x: 3x - 7 = 14",
        "Find the derivative of x² - 3x",
        "Prove by induction: 1+2+...n = n(n+1)/2"
    ]
    
    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 24) {
                    // Logo with glow
                    OrbitalLogo()
                        .frame(height: 80)
                        .padding(.top, 20)
                    
                    // Header
                    Text("ENTER YOUR MATH PROBLEM")
                        .font(.subheadline)
                        .fontWeight(.medium)
                        .foregroundStyle(OrbitalColors.textSecondaryDark)
                        .tracking(1.5)
                    
                    // Input field with purple glow
                    VStack(spacing: 0) {
                        ZStack(alignment: .topLeading) {
                            TextEditor(text: $problemText)
                                .frame(minHeight: 100, maxHeight: 150)
                                .padding()
                                .scrollContentBackground(.hidden)
                                .background(OrbitalColors.cardDark)
                                .foregroundStyle(.white)
                                .focused($isInputFocused)
                            
                            // Placeholder
                            if problemText.isEmpty {
                                Text("Find the derivative of x³ + 2x² - 5x + 1")
                                    .foregroundStyle(OrbitalColors.dimWhite)
                                    .padding(.leading, 20)
                                    .padding(.top, 24)
                                    .allowsHitTesting(false)
                            }
                        }
                        .clipShape(RoundedRectangle(cornerRadius: 16))
                        .overlay(
                            RoundedRectangle(cornerRadius: 16)
                                .stroke(OrbitalColors.accent.opacity(0.3), lineWidth: 1)
                        )
                        // Purple glow at bottom edge
                        .shadow(color: OrbitalColors.accent.opacity(0.4), radius: 12, x: 0, y: 6)
                        .shadow(color: OrbitalColors.accent.opacity(0.25), radius: 20, x: 0, y: 10)
                    }
                    .padding(.horizontal)
                    
                    // Action buttons
                    VStack(spacing: 12) {
                        // Generate Video button - Metallic silver
                        Button(action: generateVideo) {
                            HStack {
                                if isGenerating {
                                    ProgressView()
                                        .tint(.black)
                                } else {
                                    Image(systemName: "sparkles")
                                }
                                Text(isGenerating ? "Generating..." : "Generate Video")
                                    .fontWeight(.semibold)
                            }
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 16)
                            .silverButtonStyle()
                        }
                        .disabled(problemText.isEmpty || isGenerating)
                        .opacity(problemText.isEmpty ? 0.6 : 1)
                        
                        // Upload Photo button - Outline style
                        Button(action: { showingImagePicker = true }) {
                            HStack {
                                Image(systemName: "camera")
                                Text("Upload Photo")
                                    .fontWeight(.medium)
                            }
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 16)
                            .outlineButtonStyle()
                        }
                    }
                    .padding(.horizontal)
                    
                    // Tagline
                    Text("Explained step-by-step in minutes")
                        .font(.subheadline)
                        .foregroundStyle(OrbitalColors.textSecondaryDark)
                        .padding(.top, 8)
                    
                    // Example problems
                    VStack(spacing: 8) {
                        ForEach(exampleProblems, id: \.self) { example in
                            Button(action: { problemText = example }) {
                                Text(example)
                                    .font(.caption)
                                    .foregroundStyle(OrbitalColors.textSecondaryDark)
                                    .padding(.horizontal, 16)
                                    .padding(.vertical, 10)
                                    .background(OrbitalColors.cardDark)
                                    .overlay(
                                        RoundedRectangle(cornerRadius: 20)
                                            .stroke(OrbitalColors.cardBorderDark, lineWidth: 1)
                                    )
                                    .clipShape(RoundedRectangle(cornerRadius: 20))
                            }
                        }
                    }
                    .padding(.horizontal)
                    
                    Spacer(minLength: 50)
                }
            }
            .orbitalGradientBackground()
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    // Minutes balance
                    HStack(spacing: 6) {
                        Circle()
                            .fill(OrbitalColors.accent)
                            .frame(width: 8, height: 8)
                        Text("\(authManager.minutesBalance, specifier: "%.1f")")
                            .fontWeight(.semibold)
                        Text("min")
                            .foregroundStyle(OrbitalColors.textSecondaryDark)
                    }
                    .font(.subheadline)
                    .padding(.horizontal, 12)
                    .padding(.vertical, 6)
                    .background(OrbitalColors.cardDark)
                    .clipShape(Capsule())
                }
            }
            .onTapGesture {
                isInputFocused = false
            }
        }
    }
    
    func generateVideo() {
        isGenerating = true
        // TODO: Call API to generate video
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            isGenerating = false
        }
    }
}

#Preview {
    SolverView()
        .environmentObject(AuthManager())
        .preferredColorScheme(.dark)
}
