//
//  SolverView.swift
//  Orbital - AI Math Video Solver
//
//  Main solver interface where users input math problems.
//  Features:
//    - Text input with placeholder and focus glow
//    - Photo upload button (OCR coming soon)
//    - Example problem pills for quick input
//    - Minutes balance display in toolbar
//    - Animated entrance effects
//
//  Copyright © 2026 Onyx Enterprises. All rights reserved.
//

import SwiftUI

/// Primary problem input screen. Users type or photograph math problems here.
struct SolverView: View {
    @Environment(\.colorScheme) var colorScheme
    @EnvironmentObject var authManager: AuthManager
    @ObservedObject var accentTheme = AccentTheme.shared
    @State private var problemText = ""
    @State private var isGenerating = false
    @State private var showingImagePicker = false
    @FocusState private var isInputFocused: Bool
    
    // Animation states
    @State private var logoOpacity = 0.0
    @State private var logoOffset: CGFloat = 20
    @State private var contentOpacity = 0.0
    @State private var contentOffset: CGFloat = 20
    @State private var buttonsOpacity = 0.0
    @State private var buttonsOffset: CGFloat = 20
    @State private var shimmerOffset: CGFloat = -200
    
    let exampleProblems = [
        "Solve for x: 3x - 7 = 14",
        "Find the derivative of x² - 3x",
        "Prove by induction: 1+2+...n = n(n+1)/2"
    ]
    
    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 24) {
                    // Logo with breathing glow
                    BreathingLogo()
                        .frame(height: 70)
                        .padding(.top, 16)
                        .opacity(logoOpacity)
                        .offset(y: logoOffset)
                    
                    // Header
                    Text("What's the problem?")
                        .font(.system(size: 15, weight: .medium))
                        .foregroundStyle(OrbitalColors.textSecondary(colorScheme))
                        .opacity(contentOpacity)
                        .offset(y: contentOffset)
                    
                    // Input field with purple glow
                    VStack(spacing: 0) {
                        ZStack(alignment: .topLeading) {
                            TextEditor(text: $problemText)
                                .frame(minHeight: 120, maxHeight: 150)
                                .padding()
                                .scrollContentBackground(.hidden)
                                .background(OrbitalColors.card(colorScheme))
                                .foregroundStyle(OrbitalColors.textPrimary(colorScheme))
                                .font(.system(size: 17))
                                .focused($isInputFocused)
                            
                            // Placeholder
                            if problemText.isEmpty {
                                Text("Find the derivative of x³ + 2x² - 5x + 1")
                                    .foregroundStyle(OrbitalColors.dim(colorScheme))
                                    .font(.system(size: 17))
                                    .padding(.leading, 20)
                                    .padding(.top, 24)
                                    .allowsHitTesting(false)
                            }
                        }
                        .clipShape(RoundedRectangle(cornerRadius: 16))
                        .overlay(
                            RoundedRectangle(cornerRadius: 16)
                                .stroke(OrbitalColors.accent.opacity(isInputFocused ? 0.4 : 0.2), lineWidth: 1)
                        )
                        // Purple glow at bottom edge
                        .shadow(color: OrbitalColors.accent.opacity(isInputFocused ? 0.4 : 0.25), radius: isInputFocused ? 15 : 10, x: 0, y: isInputFocused ? 8 : 5)
                        .shadow(color: OrbitalColors.accent.opacity(isInputFocused ? 0.2 : 0.1), radius: 20, x: 0, y: 10)
                        .animation(.easeInOut(duration: 0.2), value: isInputFocused)
                    }
                    .padding(.horizontal)
                    .opacity(contentOpacity)
                    .offset(y: contentOffset)
                    
                    // Action buttons
                    VStack(spacing: 12) {
                        // Generate Video - Purple gradient primary CTA
                        Button(action: generateVideo) {
                            HStack(spacing: 10) {
                                if isGenerating {
                                    ProgressView()
                                        .tint(.white)
                                } else {
                                    Image(systemName: "sparkles")
                                        .font(.system(size: 16, weight: .semibold))
                                }
                                Text(isGenerating ? "Cooking up your solution..." : "Generate Video")
                                    .font(.system(size: 17, weight: .bold))
                                    .tracking(0.3)
                            }
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 16)
                            .background(
                                ZStack {
                                    LinearGradient(
                                        colors: [OrbitalColors.accentLight, OrbitalColors.accent],
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
                            .shadow(color: OrbitalColors.accent.opacity(0.5), radius: 12, x: 0, y: 6)
                            .shadow(color: OrbitalColors.accent.opacity(0.3), radius: 20, x: 0, y: 10)
                        }
                        .disabled(problemText.isEmpty || isGenerating)
                        .opacity(problemText.isEmpty ? 0.5 : 1)
                        .onAppear {
                            withAnimation(.linear(duration: 2.5).repeatForever(autoreverses: false)) {
                                shimmerOffset = 400
                            }
                        }
                        
                        // Upload Photo - Outline style
                        Button(action: { 
                            let generator = UIImpactFeedbackGenerator(style: .light)
                            generator.impactOccurred()
                            showingImagePicker = true 
                        }) {
                            HStack(spacing: 10) {
                                Text("📸")
                                    .font(.system(size: 18))
                                Text("Upload Photo")
                                    .font(.system(size: 16, weight: .semibold))
                            }
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 16)
                            .background(OrbitalColors.card(colorScheme))
                            .foregroundStyle(OrbitalColors.textPrimary(colorScheme))
                            .clipShape(RoundedRectangle(cornerRadius: 12))
                            .overlay(
                                RoundedRectangle(cornerRadius: 12)
                                    .stroke(OrbitalColors.cardBorder(colorScheme), lineWidth: 1)
                            )
                        }
                    }
                    .padding(.horizontal)
                    .opacity(buttonsOpacity)
                    .offset(y: buttonsOffset)
                    
                    // Tagline
                    Text("Math in minutes. Value your time.")
                        .font(.subheadline)
                        .foregroundStyle(OrbitalColors.textSecondary(colorScheme))
                        .padding(.top, 8)
                        .opacity(buttonsOpacity)
                        .offset(y: buttonsOffset)
                    
                    // Example problems - horizontal scroll
                    ScrollView(.horizontal, showsIndicators: false) {
                        HStack(spacing: 10) {
                            ForEach(exampleProblems, id: \.self) { example in
                                Button(action: { 
                                    let generator = UIImpactFeedbackGenerator(style: .light)
                                    generator.impactOccurred()
                                    withAnimation(.easeInOut(duration: 0.2)) {
                                        problemText = example 
                                    }
                                }) {
                                    Text(example)
                                        .font(.caption)
                                        .foregroundStyle(OrbitalColors.textSecondary(colorScheme))
                                        .padding(.horizontal, 16)
                                        .padding(.vertical, 10)
                                        .background(OrbitalColors.card(colorScheme))
                                        .clipShape(Capsule())
                                        .overlay(
                                            Capsule()
                                                .stroke(OrbitalColors.cardBorder(colorScheme), lineWidth: 1)
                                        )
                                }
                            }
                        }
                        .padding(.horizontal)
                    }
                    .opacity(buttonsOpacity)
                    .offset(y: buttonsOffset)
                    
                    Spacer(minLength: 50)
                }
            }
            .orbitalGradientBackground()
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    // Minutes balance pill
                    HStack(spacing: 6) {
                        Circle()
                            .fill(OrbitalColors.accent)
                            .frame(width: 8, height: 8)
                            .shadow(color: OrbitalColors.accent.opacity(0.5), radius: 4)
                        Text("\(authManager.minutesBalance, specifier: "%.1f")")
                            .fontWeight(.semibold)
                            .foregroundStyle(OrbitalColors.textPrimary(colorScheme))
                        Text("min")
                            .foregroundStyle(OrbitalColors.textSecondary(colorScheme))
                    }
                    .font(.subheadline)
                    .padding(.horizontal, 14)
                    .padding(.vertical, 8)
                    .background(OrbitalColors.card(colorScheme))
                    .clipShape(Capsule())
                    .overlay(
                        Capsule()
                            .stroke(OrbitalColors.cardBorder(colorScheme), lineWidth: 1)
                    )
                }
            }
            .onTapGesture {
                isInputFocused = false
            }
            .onAppear {
                startEntranceAnimations()
            }
        }
    }
    
    func startEntranceAnimations() {
        withAnimation(.easeOut(duration: 0.6)) {
            logoOpacity = 1
            logoOffset = 0
        }
        
        withAnimation(.easeOut(duration: 0.6).delay(0.15)) {
            contentOpacity = 1
            contentOffset = 0
        }
        
        withAnimation(.easeOut(duration: 0.6).delay(0.3)) {
            buttonsOpacity = 1
            buttonsOffset = 0
        }
    }
    
    func generateVideo() {
        let generator = UIImpactFeedbackGenerator(style: .medium)
        generator.impactOccurred()
        
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
