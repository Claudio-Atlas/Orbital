//
//  AccentColorPicker.swift
//  Orbital - AI Math Video Solver
//
//  Accent color selection UI for Settings.
//  Displays color swatches in a horizontal row.
//
//  Copyright © 2026 Onyx Enterprises. All rights reserved.
//

import SwiftUI

/// Horizontal row of color swatches for accent color selection
struct AccentColorPicker: View {
    @ObservedObject var accentTheme = AccentTheme.shared
    @Environment(\.colorScheme) var colorScheme
    
    var body: some View {
        HStack(spacing: 12) {
            ForEach(AccentPreset.allCases) { preset in
                AccentSwatch(
                    preset: preset,
                    isSelected: accentTheme.preset == preset,
                    colorScheme: colorScheme
                ) {
                    withAnimation(.spring(response: 0.3, dampingFraction: 0.7)) {
                        accentTheme.preset = preset
                        // Haptic feedback
                        let generator = UIImpactFeedbackGenerator(style: .light)
                        generator.impactOccurred()
                    }
                }
            }
        }
    }
}

/// Individual color swatch button
struct AccentSwatch: View {
    let preset: AccentPreset
    let isSelected: Bool
    let colorScheme: ColorScheme
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            ZStack {
                // Outer glow when selected
                if isSelected {
                    Circle()
                        .fill(preset.color.opacity(0.3))
                        .frame(width: 40, height: 40)
                }
                
                // Main color circle
                Circle()
                    .fill(
                        LinearGradient(
                            colors: [preset.colorLight, preset.color],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    )
                    .frame(width: 32, height: 32)
                    .shadow(color: preset.color.opacity(isSelected ? 0.5 : 0.2), radius: isSelected ? 8 : 4)
                
                // Checkmark when selected
                if isSelected {
                    Image(systemName: "checkmark")
                        .font(.system(size: 14, weight: .bold))
                        .foregroundStyle(.white)
                }
            }
            .frame(width: 40, height: 40)
        }
        .buttonStyle(.plain)
    }
}

/// Full-screen accent color picker (alternative layout)
struct AccentColorPickerSheet: View {
    @ObservedObject var accentTheme = AccentTheme.shared
    @Environment(\.colorScheme) var colorScheme
    @Environment(\.dismiss) var dismiss
    
    var body: some View {
        NavigationStack {
            VStack(spacing: 32) {
                // Preview
                VStack(spacing: 16) {
                    // Logo preview with current accent glow
                    BreathingLogo()
                        .frame(height: 100)
                    
                    Text("Preview")
                        .font(.caption)
                        .foregroundStyle(OrbitalColors.textSecondary(colorScheme))
                }
                .padding(.top, 20)
                
                // Color grid
                LazyVGrid(columns: [
                    GridItem(.flexible()),
                    GridItem(.flexible()),
                    GridItem(.flexible())
                ], spacing: 20) {
                    ForEach(AccentPreset.allCases) { preset in
                        AccentOptionCard(
                            preset: preset,
                            isSelected: accentTheme.preset == preset,
                            colorScheme: colorScheme
                        ) {
                            withAnimation(.spring(response: 0.3, dampingFraction: 0.7)) {
                                accentTheme.preset = preset
                                let generator = UIImpactFeedbackGenerator(style: .medium)
                                generator.impactOccurred()
                            }
                        }
                    }
                }
                .padding(.horizontal)
                
                Spacer()
            }
            .orbitalGradientBackground()
            .navigationTitle("Accent Color")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button("Done") {
                        dismiss()
                    }
                    .foregroundStyle(accentTheme.color)
                }
            }
        }
    }
}

/// Card-style accent option for the sheet
struct AccentOptionCard: View {
    let preset: AccentPreset
    let isSelected: Bool
    let colorScheme: ColorScheme
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            VStack(spacing: 8) {
                ZStack {
                    Circle()
                        .fill(
                            LinearGradient(
                                colors: [preset.colorLight, preset.color],
                                startPoint: .topLeading,
                                endPoint: .bottomTrailing
                            )
                        )
                        .frame(width: 50, height: 50)
                        .shadow(color: preset.color.opacity(0.4), radius: 8)
                    
                    if isSelected {
                        Image(systemName: "checkmark")
                            .font(.system(size: 20, weight: .bold))
                            .foregroundStyle(.white)
                    }
                }
                
                Text(preset.displayName)
                    .font(.caption)
                    .foregroundStyle(OrbitalColors.textPrimary(colorScheme))
                    .lineLimit(1)
            }
            .padding(.vertical, 16)
            .padding(.horizontal, 8)
            .frame(maxWidth: .infinity)
            .background(OrbitalColors.card(colorScheme))
            .clipShape(RoundedRectangle(cornerRadius: 16))
            .overlay(
                RoundedRectangle(cornerRadius: 16)
                    .stroke(isSelected ? preset.color : OrbitalColors.cardBorder(colorScheme), lineWidth: isSelected ? 2 : 1)
            )
        }
        .buttonStyle(.plain)
    }
}

#Preview {
    AccentColorPickerSheet()
        .preferredColorScheme(.dark)
}
