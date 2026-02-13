import SwiftUI

struct OrbitalColors {
    // Primary accent - purple/violet
    static let accent = Color(red: 139/255, green: 92/255, blue: 246/255)
    static let accentLight = Color(red: 167/255, green: 139/255, blue: 250/255)
    
    // Whites
    static let neonWhiteBright = Color.white
    static let neonWhite = Color(white: 0.9)
    static let dimWhite = Color(white: 0.45)
    
    // Borders
    static let inputBorder = Color(white: 0.2)
    
    // Backgrounds
    static let backgroundDark = Color.black
    static let cardDark = Color(white: 0.05)
    static let cardBorderDark = Color(white: 0.15)
    
    // Light mode
    static let backgroundLight = Color(white: 0.98)
    static let cardLight = Color.white
    static let cardBorderLight = Color(white: 0.9)
    
    // Text
    static let textPrimaryDark = Color.white
    static let textSecondaryDark = Color(white: 0.55)
    static let textPrimaryLight = Color(white: 0.1)
    static let textSecondaryLight = Color(white: 0.45)
    
    // Status
    static let warning = Color(red: 245/255, green: 158/255, blue: 11/255)
    static let success = Color(red: 34/255, green: 197/255, blue: 94/255)
    static let error = Color(red: 239/255, green: 68/255, blue: 68/255)
    
    // Deep Space gradient
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
}

// MARK: - View Modifiers

extension View {
    func orbitalBackground() -> some View {
        self.modifier(OrbitalBackgroundModifier())
    }
    
    func orbitalGradientBackground() -> some View {
        self.background(OrbitalColors.deepSpaceGradient)
    }
    
    func orbitalCard() -> some View {
        self.modifier(OrbitalCardModifier())
    }
    
    func neonInputStyle() -> some View {
        self.modifier(NeonInputModifier())
    }
    
    func silverButtonStyle() -> some View {
        self.modifier(SilverButtonModifier())
    }
    
    func outlineButtonStyle() -> some View {
        self.modifier(OutlineButtonModifier())
    }
}

struct OrbitalBackgroundModifier: ViewModifier {
    @Environment(\.colorScheme) var colorScheme
    
    func body(content: Content) -> some View {
        content
            .background(colorScheme == .dark ? OrbitalColors.backgroundDark : OrbitalColors.backgroundLight)
    }
}

struct OrbitalCardModifier: ViewModifier {
    @Environment(\.colorScheme) var colorScheme
    
    func body(content: Content) -> some View {
        content
            .background(colorScheme == .dark ? OrbitalColors.cardDark : OrbitalColors.cardLight)
            .clipShape(RoundedRectangle(cornerRadius: 16))
            .overlay(
                RoundedRectangle(cornerRadius: 16)
                    .stroke(colorScheme == .dark ? OrbitalColors.cardBorderDark : OrbitalColors.cardBorderLight, lineWidth: 1)
            )
    }
}

struct NeonInputModifier: ViewModifier {
    func body(content: Content) -> some View {
        content
            .background(OrbitalColors.cardDark)
            .clipShape(RoundedRectangle(cornerRadius: 12))
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(OrbitalColors.accent.opacity(0.2), lineWidth: 1)
            )
            // Purple glow at bottom - turned up slightly
            .shadow(color: OrbitalColors.accent.opacity(0.2), radius: 10, x: 0, y: 5)
            .shadow(color: OrbitalColors.accent.opacity(0.1), radius: 16, x: 0, y: 8)
    }
}

struct SilverButtonModifier: ViewModifier {
    func body(content: Content) -> some View {
        content
            .background(
                ZStack {
                    LinearGradient(
                        stops: [
                            .init(color: Color(white: 0.95), location: 0),
                            .init(color: Color(white: 0.85), location: 0.3),
                            .init(color: Color(white: 0.75), location: 0.7),
                            .init(color: Color(white: 0.65), location: 1),
                        ],
                        startPoint: .top,
                        endPoint: .bottom
                    )
                    VStack {
                        LinearGradient(
                            colors: [Color.white.opacity(0.4), Color.clear],
                            startPoint: .top,
                            endPoint: .bottom
                        )
                        .frame(height: 20)
                        Spacer()
                    }
                }
            )
            .foregroundStyle(.black)
            .clipShape(RoundedRectangle(cornerRadius: 12))
    }
}

struct OutlineButtonModifier: ViewModifier {
    func body(content: Content) -> some View {
        content
            .background(OrbitalColors.cardDark)
            .foregroundStyle(.white)
            .clipShape(RoundedRectangle(cornerRadius: 12))
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(Color.white.opacity(0.15), lineWidth: 1)
            )
    }
}
