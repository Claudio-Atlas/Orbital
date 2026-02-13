//
//  OrbitalLogo.swift
//  Orbital - AI Math Video Solver
//
//  Reusable logo components with adaptive dark/light mode support.
//
//  Components:
//    - OrbitalLogo: Static logo that adapts to color scheme
//    - BreathingLogo: Animated logo with pulsing purple glow
//
//  Copyright © 2026 Onyx Enterprises. All rights reserved.
//

import SwiftUI

/// Static logo component that switches between light/dark variants.
struct OrbitalLogo: View {
    @Environment(\.colorScheme) var colorScheme
    
    var body: some View {
        Image(colorScheme == .dark ? "OrbitalLogo" : "OrbitalLogoDark")
            .resizable()
            .aspectRatio(contentMode: .fit)
    }
}

/// Animated logo with a pulsing purple glow effect (3-layer shadow).
/// Used on login, solver, library, and profile screens.
struct BreathingLogo: View {
    @Environment(\.colorScheme) var colorScheme
    @State private var glowIntensity: Double = 0.6
    
    var body: some View {
        Image(colorScheme == .dark ? "OrbitalLogo" : "OrbitalLogoDark")
            .resizable()
            .aspectRatio(contentMode: .fit)
            .shadow(color: OrbitalColors.accent.opacity(0.6 * glowIntensity), radius: 25, x: 0, y: 0)
            .shadow(color: OrbitalColors.accent.opacity(0.4 * glowIntensity), radius: 45, x: 0, y: 0)
            .shadow(color: OrbitalColors.accent.opacity(0.2 * glowIntensity), radius: 70, x: 0, y: 0)
            .onAppear {
                withAnimation(.easeInOut(duration: 2.0).repeatForever(autoreverses: true)) {
                    glowIntensity = 1.0
                }
            }
    }
}

#Preview {
    VStack(spacing: 40) {
        BreathingLogo()
            .frame(width: 150, height: 150)
    }
    .padding()
    .background(Color.black)
}
