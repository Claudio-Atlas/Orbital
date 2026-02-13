//
//  LibraryView.swift
//  Orbital - AI Math Video Solver
//
//  Video library showing user's solved problems. Features:
//    - Videos/Steps toggle view mode
//    - Search functionality
//    - "Continue" card for most recent solve
//    - Expiration warnings (videos auto-delete after 48h)
//    - Empty state for new users
//
//  Copyright © 2026 Onyx Enterprises. All rights reserved.
//

import SwiftUI

/// Library of user's generated solution videos.
struct LibraryView: View {
    @Environment(\.colorScheme) var colorScheme
    @State private var videos: [Video] = Video.sampleVideos
    @State private var showingSteps = false
    @State private var searchText = ""
    
    // Animation states
    @State private var headerOpacity = 0.0
    @State private var headerOffset: CGFloat = 20
    @State private var contentOpacity = 0.0
    @State private var contentOffset: CGFloat = 20
    
    var filteredVideos: [Video] {
        if searchText.isEmpty {
            return videos
        }
        return videos.filter { $0.problem.localizedCaseInsensitiveContains(searchText) }
    }
    
    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 20) {
                    // Logo
                    BreathingLogo()
                        .frame(height: 50)
                        .padding(.top, 10)
                        .opacity(headerOpacity)
                        .offset(y: headerOffset)
                    
                    // Header
                    VStack(spacing: 4) {
                        Text("Your Solves")
                            .font(.system(size: 24, weight: .bold))
                            .foregroundStyle(OrbitalColors.textPrimary(colorScheme))
                        Text("Your explained problems")
                            .font(.subheadline)
                            .foregroundStyle(OrbitalColors.textSecondary(colorScheme))
                    }
                    .opacity(headerOpacity)
                    .offset(y: headerOffset)
                    
                    // Toggle: Videos | Steps
                    Picker("View Mode", selection: $showingSteps) {
                        Text("Videos").tag(false)
                        Text("Steps").tag(true)
                    }
                    .pickerStyle(.segmented)
                    .padding(.horizontal)
                    .opacity(contentOpacity)
                    .offset(y: contentOffset)
                    
                    // Search bar with purple glow
                    HStack {
                        Image(systemName: "magnifyingglass")
                            .foregroundStyle(OrbitalColors.dim(colorScheme))
                        
                        ZStack(alignment: .leading) {
                            if searchText.isEmpty {
                                Text("Search problems...")
                                    .foregroundStyle(OrbitalColors.dim(colorScheme))
                            }
                            TextField("", text: $searchText)
                                .foregroundStyle(OrbitalColors.textPrimary(colorScheme))
                                .tint(OrbitalColors.accent)
                        }
                    }
                    .padding()
                    .background(OrbitalColors.card(colorScheme))
                    .clipShape(RoundedRectangle(cornerRadius: 12))
                    .overlay(
                        RoundedRectangle(cornerRadius: 12)
                            .stroke(OrbitalColors.accent.opacity(0.2), lineWidth: 1)
                    )
                    .shadow(color: OrbitalColors.accent.opacity(0.15), radius: 8, x: 0, y: 4)
                    .padding(.horizontal)
                    .opacity(contentOpacity)
                    .offset(y: contentOffset)
                    
                    if filteredVideos.isEmpty {
                        // Empty state
                        LibraryEmptyStateView(colorScheme: colorScheme)
                            .padding(.top, 60)
                            .opacity(contentOpacity)
                            .offset(y: contentOffset)
                    } else {
                        // Continue section (most recent)
                        if let lastVideo = filteredVideos.first {
                            LibraryContinueCard(video: lastVideo, showingSteps: showingSteps, colorScheme: colorScheme)
                                .padding(.horizontal)
                                .opacity(contentOpacity)
                                .offset(y: contentOffset)
                        }
                        
                        // Video list
                        LazyVStack(spacing: 12) {
                            ForEach(filteredVideos.dropFirst()) { video in
                                LibraryVideoCard(video: video, showingSteps: showingSteps, colorScheme: colorScheme)
                            }
                        }
                        .padding(.horizontal)
                        .opacity(contentOpacity)
                        .offset(y: contentOffset)
                    }
                    
                    Spacer(minLength: 50)
                }
            }
            .orbitalGradientBackground()
            .onAppear {
                startEntranceAnimations()
            }
        }
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
}

// MARK: - Continue Card
struct LibraryContinueCard: View {
    let video: Video
    let showingSteps: Bool
    let colorScheme: ColorScheme
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Continue")
                .font(.caption)
                .fontWeight(.medium)
                .foregroundStyle(OrbitalColors.accent)
            
            Text(video.problem)
                .font(.headline)
                .foregroundStyle(OrbitalColors.textPrimary(colorScheme))
                .lineLimit(2)
            
            HStack {
                Text(video.category)
                    .font(.caption)
                    .foregroundStyle(OrbitalColors.accent)
                
                Text("•")
                    .foregroundStyle(OrbitalColors.textSecondary(colorScheme))
                
                Text(video.subcategory)
                    .font(.caption)
                    .foregroundStyle(OrbitalColors.textSecondary(colorScheme))
                
                Spacer()
                
                Text(video.durationFormatted)
                    .font(.caption)
                    .foregroundStyle(OrbitalColors.textSecondary(colorScheme))
            }
            
            if showingSteps {
                Divider()
                    .background(OrbitalColors.cardBorder(colorScheme))
                
                VStack(alignment: .leading, spacing: 4) {
                    ForEach(Array(video.stepPreview.prefix(2).enumerated()), id: \.offset) { index, step in
                        Text("\(index + 1). \(step)")
                            .font(.caption)
                            .foregroundStyle(OrbitalColors.textSecondary(colorScheme))
                    }
                    
                    if let result = video.result {
                        Text("Result: \(result)")
                            .font(.caption)
                            .fontWeight(.medium)
                            .foregroundStyle(OrbitalColors.textPrimary(colorScheme))
                    }
                }
            }
            
            if video.hoursUntilExpiration < 24 {
                HStack {
                    Image(systemName: "clock")
                    Text("\(video.hoursUntilExpiration)h left")
                }
                .font(.caption)
                .foregroundStyle(OrbitalColors.warning)
            }
        }
        .padding()
        .background(OrbitalColors.card(colorScheme))
        .clipShape(RoundedRectangle(cornerRadius: 16))
        .overlay(
            RoundedRectangle(cornerRadius: 16)
                .stroke(OrbitalColors.accent.opacity(0.2), lineWidth: 1)
        )
        .shadow(color: OrbitalColors.accent.opacity(0.2), radius: 12, x: 0, y: 4)
    }
}

// MARK: - Video Card
struct LibraryVideoCard: View {
    let video: Video
    let showingSteps: Bool
    let colorScheme: ColorScheme
    
    var body: some View {
        HStack(alignment: .top, spacing: 14) {
            // Play button
            ZStack {
                Circle()
                    .fill(
                        LinearGradient(
                            colors: [OrbitalColors.accentLight, OrbitalColors.accent],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    )
                    .frame(width: 36, height: 36)
                    .shadow(color: OrbitalColors.accent.opacity(0.4), radius: 6)
                
                Image(systemName: "play.fill")
                    .font(.system(size: 12))
                    .foregroundStyle(.white)
                    .offset(x: 1)
            }
            .padding(.top, 2)
            
            VStack(alignment: .leading, spacing: 8) {
                Text(video.problem)
                    .font(.subheadline)
                    .fontWeight(.medium)
                    .foregroundStyle(OrbitalColors.textPrimary(colorScheme))
                    .lineLimit(2)
                
                HStack {
                    Text(video.category)
                        .font(.caption)
                        .foregroundStyle(OrbitalColors.accent)
                    
                    Text("•")
                        .foregroundStyle(OrbitalColors.textSecondary(colorScheme))
                    
                    Text(video.subcategory)
                        .font(.caption)
                        .foregroundStyle(OrbitalColors.textSecondary(colorScheme))
                    
                    Spacer()
                    
                    Text(video.durationFormatted)
                        .font(.caption)
                        .foregroundStyle(OrbitalColors.textSecondary(colorScheme))
                }
                
                if showingSteps {
                    VStack(alignment: .leading, spacing: 2) {
                        ForEach(Array(video.stepPreview.prefix(2).enumerated()), id: \.offset) { index, step in
                            Text("\(index + 1). \(step)")
                                .font(.caption2)
                                .foregroundStyle(OrbitalColors.textSecondary(colorScheme))
                        }
                        
                        if let result = video.result {
                            Text("Result: \(result)")
                                .font(.caption2)
                                .fontWeight(.medium)
                                .foregroundStyle(OrbitalColors.textPrimary(colorScheme))
                        }
                    }
                    .padding(.top, 4)
                }
            }
        }
        .padding()
        .background(OrbitalColors.card(colorScheme))
        .clipShape(RoundedRectangle(cornerRadius: 16))
        .overlay(
            RoundedRectangle(cornerRadius: 16)
                .stroke(OrbitalColors.cardBorder(colorScheme), lineWidth: 1)
        )
    }
}

// MARK: - Empty State
struct LibraryEmptyStateView: View {
    let colorScheme: ColorScheme
    
    var body: some View {
        VStack(spacing: 16) {
            ZStack {
                Circle()
                    .fill(OrbitalColors.accent.opacity(0.1))
                    .frame(width: 80, height: 80)
                
                Image(systemName: "play.rectangle.on.rectangle")
                    .font(.system(size: 32))
                    .foregroundStyle(OrbitalColors.accent)
            }
            
            Text("No solves yet")
                .font(.headline)
                .foregroundStyle(OrbitalColors.textPrimary(colorScheme))
            
            Text("Go crush some math! 💪")
                .font(.subheadline)
                .foregroundStyle(OrbitalColors.textSecondary(colorScheme))
        }
    }
}

#Preview {
    LibraryView()
        .preferredColorScheme(.dark)
}
