//
//  OrbitalColors.swift
//  Orbital - AI Math Video Solver
//
//  Design system colors and view modifiers. Tesla-inspired dark theme
//  with purple accents and adaptive light mode support.
//
//  Usage:
//    - Colors: OrbitalColors.accent, OrbitalColors.textPrimary(colorScheme)
//    - Modifiers: .orbitalCard(), .orbitalGradientBackground()
//
//  Copyright © 2026 Onyx Enterprises. All rights reserved.
//

import SwiftUI

/// Centralized color definitions for the Orbital design system.
/// All colors support both dark and light mode via adaptive helper functions.
struct OrbitalColors {
    // Primary accent - now dynamic via AccentTheme
    static var accent: Color { AccentTheme.shared.color }
    static var accentLight: Color { AccentTheme.shared.colorLight }
    
    // Accent gradient
    static var accentGradient: LinearGradient { AccentTheme.shared.gradient }
    static var accentHorizontalGradient: LinearGradient { AccentTheme.shared.horizontalGradient }
    
    // Whites
    static let neonWhiteBright = Color.white
    static let neonWhite = Color(white: 0.9)
    static let dimWhite = Color(white: 0.45)
    
    // Backgrounds - Dark mode
    static let backgroundDark = Color.black
    static let cardDark = Color(white: 0.05)
    static let cardBorderDark = Color(white: 0.15)
    
    // Backgrounds - Light mode
    static let backgroundLight = Color(white: 0.98)
    static let cardLight = Color.white
    static let cardBorderLight = Color(white: 0.88)
    
    // Text - Dark mode
    static let textPrimaryDark = Color.white
    static let textSecondaryDark = Color(white: 0.55)
    
    // Text - Light mode  
    static let textPrimaryLight = Color(white: 0.1)
    static let textSecondaryLight = Color(white: 0.45)
    
    // Dim colors for placeholders
    static let dimWhiteLight = Color(white: 0.6)
    
    // Status
    static let warning = Color(red: 245/255, green: 158/255, blue: 11/255)
    static let success = Color(red: 34/255, green: 197/255, blue: 94/255)
    static let error = Color(red: 239/255, green: 68/255, blue: 68/255)
    
    // Deep Space gradient (dark mode)
    static var deepSpaceGradient: LinearGradient {
        LinearGradient(
            colors: [
                Color(red: 10/255, green: 10/255, blue: 20/255),
                Color(red: 2/255, green: 2/255, blue: 4/255),
            ],
            startPoint: .top,
            endPoint: .bottom
        )
    }
    
    // Light gradient (light mode)
    static var lightGradient: LinearGradient {
        LinearGradient(
            colors: [
                Color(white: 0.98),
                Color(white: 0.94),
            ],
            startPoint: .top,
            endPoint: .bottom
        )
    }
    
    // MARK: - Adaptive Colors
    
    static func card(_ colorScheme: ColorScheme) -> Color {
        colorScheme == .dark ? cardDark : cardLight
    }
    
    static func cardBorder(_ colorScheme: ColorScheme) -> Color {
        colorScheme == .dark ? cardBorderDark : cardBorderLight
    }
    
    static func textPrimary(_ colorScheme: ColorScheme) -> Color {
        colorScheme == .dark ? textPrimaryDark : textPrimaryLight
    }
    
    static func textSecondary(_ colorScheme: ColorScheme) -> Color {
        colorScheme == .dark ? textSecondaryDark : textSecondaryLight
    }
    
    static func dim(_ colorScheme: ColorScheme) -> Color {
        colorScheme == .dark ? dimWhite : dimWhiteLight
    }
    
    static func background(_ colorScheme: ColorScheme) -> AnyShapeStyle {
        colorScheme == .dark ? AnyShapeStyle(deepSpaceGradient) : AnyShapeStyle(lightGradient)
    }
}

// MARK: - View Modifiers

extension View {
    func orbitalBackground() -> some View {
        self.modifier(OrbitalBackgroundModifier())
    }
    
    func orbitalGradientBackground() -> some View {
        self.modifier(OrbitalGradientBackgroundModifier())
    }
    
    func orbitalCard() -> some View {
        self.modifier(OrbitalCardModifier())
    }
}

struct OrbitalBackgroundModifier: ViewModifier {
    @Environment(\.colorScheme) var colorScheme
    
    func body(content: Content) -> some View {
        content
            .background(colorScheme == .dark ? OrbitalColors.backgroundDark : OrbitalColors.backgroundLight)
    }
}

struct OrbitalGradientBackgroundModifier: ViewModifier {
    @Environment(\.colorScheme) var colorScheme
    
    func body(content: Content) -> some View {
        content
            .background(OrbitalColors.background(colorScheme))
    }
}

struct OrbitalCardModifier: ViewModifier {
    @Environment(\.colorScheme) var colorScheme
    
    func body(content: Content) -> some View {
        content
            .background(OrbitalColors.card(colorScheme))
            .clipShape(RoundedRectangle(cornerRadius: 16))
            .overlay(
                RoundedRectangle(cornerRadius: 16)
                    .stroke(OrbitalColors.cardBorder(colorScheme), lineWidth: 1)
            )
    }
}
