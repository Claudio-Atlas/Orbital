//
//  AccentTheme.swift
//  Orbital - AI Math Video Solver
//
//  User-selectable accent colors for personalization.
//  Supports college/school branding through color presets.
//
//  Usage:
//    @StateObject var accentTheme = AccentTheme.shared
//    .tint(accentTheme.color)
//
//  Copyright © 2026 Onyx Enterprises. All rights reserved.
//

import SwiftUI

/// Available accent color presets
enum AccentPreset: String, CaseIterable, Identifiable {
    case nebulaPurple = "nebulaPurple"
    case oceanBlue = "oceanBlue"
    case cardinalRed = "cardinalRed"
    case forestGreen = "forestGreen"
    case sunsetOrange = "sunsetOrange"
    case electricPink = "electricPink"
    case cyberCyan = "cyberCyan"
    
    var id: String { rawValue }
    
    /// Display name for the picker
    var displayName: String {
        switch self {
        case .nebulaPurple: return "Nebula Purple"
        case .oceanBlue: return "Ocean Blue"
        case .cardinalRed: return "Cardinal Red"
        case .forestGreen: return "Forest Green"
        case .sunsetOrange: return "Sunset Orange"
        case .electricPink: return "Electric Pink"
        case .cyberCyan: return "Cyber Cyan"
        }
    }
    
    /// Primary accent color
    var color: Color {
        switch self {
        case .nebulaPurple: return Color(red: 139/255, green: 92/255, blue: 246/255)
        case .oceanBlue: return Color(red: 59/255, green: 130/255, blue: 246/255)
        case .cardinalRed: return Color(red: 239/255, green: 68/255, blue: 68/255)
        case .forestGreen: return Color(red: 34/255, green: 197/255, blue: 94/255)
        case .sunsetOrange: return Color(red: 249/255, green: 115/255, blue: 22/255)
        case .electricPink: return Color(red: 236/255, green: 72/255, blue: 153/255)
        case .cyberCyan: return Color(red: 6/255, green: 182/255, blue: 212/255)
        }
    }
    
    /// Lighter variant for gradients
    var colorLight: Color {
        switch self {
        case .nebulaPurple: return Color(red: 167/255, green: 139/255, blue: 250/255)
        case .oceanBlue: return Color(red: 96/255, green: 165/255, blue: 250/255)
        case .cardinalRed: return Color(red: 252/255, green: 129/255, blue: 129/255)
        case .forestGreen: return Color(red: 74/255, green: 222/255, blue: 128/255)
        case .sunsetOrange: return Color(red: 253/255, green: 186/255, blue: 116/255)
        case .electricPink: return Color(red: 244/255, green: 114/255, blue: 182/255)
        case .cyberCyan: return Color(red: 103/255, green: 232/255, blue: 249/255)
        }
    }
}

/// Observable object that manages the user's accent color preference.
/// Uses @AppStorage for persistence across app launches.
class AccentTheme: ObservableObject {
    static let shared = AccentTheme()
    
    @AppStorage("accentPreset") private var storedPreset: String = AccentPreset.nebulaPurple.rawValue
    
    /// Current accent preset
    var preset: AccentPreset {
        get { AccentPreset(rawValue: storedPreset) ?? .nebulaPurple }
        set {
            storedPreset = newValue.rawValue
            objectWillChange.send()
        }
    }
    
    /// Current accent color
    var color: Color { preset.color }
    
    /// Current accent color (light variant)
    var colorLight: Color { preset.colorLight }
    
    /// Gradient from light to main accent
    var gradient: LinearGradient {
        LinearGradient(
            colors: [preset.colorLight, preset.color],
            startPoint: .topLeading,
            endPoint: .bottomTrailing
        )
    }
    
    /// Horizontal gradient for buttons
    var horizontalGradient: LinearGradient {
        LinearGradient(
            colors: [preset.colorLight, preset.color],
            startPoint: .leading,
            endPoint: .trailing
        )
    }
    
    private init() {}
}
