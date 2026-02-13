import SwiftUI

struct LibraryView: View {
    @Environment(\.colorScheme) var colorScheme
    @State private var videos: [Video] = Video.sampleVideos
    @State private var showingSteps = false
    @State private var searchText = ""
    
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
                    OrbitalLogo()
                        .frame(height: 60)
                        .padding(.top, 10)
                    
                    // Header
                    VStack(spacing: 4) {
                        Text(showingSteps ? "Solution Library" : "Video Library")
                            .font(.title2)
                            .fontWeight(.bold)
                        Text("Your explained problems")
                            .font(.subheadline)
                            .foregroundStyle(colorScheme == .dark ? OrbitalColors.textSecondaryDark : OrbitalColors.textSecondaryLight)
                    }
                    
                    // Toggle: Solver | Solution Library
                    Picker("View Mode", selection: $showingSteps) {
                        Text("Solver").tag(false)
                        Text("Solution Library").tag(true)
                    }
                    .pickerStyle(.segmented)
                    .padding(.horizontal)
                    
                    // Search bar
                    HStack {
                        Image(systemName: "magnifyingglass")
                            .foregroundStyle(colorScheme == .dark ? OrbitalColors.textSecondaryDark : OrbitalColors.textSecondaryLight)
                        TextField("Search problems...", text: $searchText)
                    }
                    .padding()
                    .background(colorScheme == .dark ? OrbitalColors.cardDark : OrbitalColors.cardLight)
                    .clipShape(RoundedRectangle(cornerRadius: 12))
                    .overlay(
                        RoundedRectangle(cornerRadius: 12)
                            .stroke(colorScheme == .dark ? OrbitalColors.cardBorderDark : OrbitalColors.cardBorderLight, lineWidth: 1)
                    )
                    .padding(.horizontal)
                    
                    // Continue section (most recent)
                    if let lastVideo = videos.first {
                        ContinueCard(video: lastVideo, showingSteps: showingSteps)
                            .padding(.horizontal)
                    }
                    
                    // Video list
                    LazyVStack(spacing: 12) {
                        ForEach(filteredVideos.dropFirst()) { video in
                            VideoCard(video: video, showingSteps: showingSteps)
                        }
                    }
                    .padding(.horizontal)
                    
                    if filteredVideos.isEmpty {
                        EmptyStateView()
                            .padding(.top, 40)
                    }
                    
                    Spacer(minLength: 50)
                }
            }
            .orbitalBackground()
        }
    }
}

// MARK: - Continue Card (Featured/Last Watched)
struct ContinueCard: View {
    let video: Video
    let showingSteps: Bool
    @Environment(\.colorScheme) var colorScheme
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Continue")
                .font(.caption)
                .foregroundStyle(colorScheme == .dark ? OrbitalColors.textSecondaryDark : OrbitalColors.textSecondaryLight)
            
            Text(video.problem)
                .font(.headline)
                .lineLimit(2)
            
            HStack {
                Text(video.category)
                    .font(.caption)
                    .foregroundStyle(OrbitalColors.accent)
                
                Text("•")
                    .foregroundStyle(colorScheme == .dark ? OrbitalColors.textSecondaryDark : OrbitalColors.textSecondaryLight)
                
                Text(video.subcategory)
                    .font(.caption)
                    .foregroundStyle(colorScheme == .dark ? OrbitalColors.textSecondaryDark : OrbitalColors.textSecondaryLight)
                
                Spacer()
                
                Text(video.durationFormatted)
                    .font(.caption)
                    .foregroundStyle(colorScheme == .dark ? OrbitalColors.textSecondaryDark : OrbitalColors.textSecondaryLight)
            }
            
            if showingSteps {
                Divider()
                    .background(colorScheme == .dark ? OrbitalColors.cardBorderDark : OrbitalColors.cardBorderLight)
                
                // Show step preview
                VStack(alignment: .leading, spacing: 4) {
                    ForEach(Array(video.stepPreview.prefix(2).enumerated()), id: \.offset) { index, step in
                        Text("\(index + 1). \(step)")
                            .font(.caption)
                            .foregroundStyle(colorScheme == .dark ? OrbitalColors.textSecondaryDark : OrbitalColors.textSecondaryLight)
                    }
                    
                    if let result = video.result {
                        Text("Result: \(result)")
                            .font(.caption)
                            .fontWeight(.medium)
                    }
                }
            }
            
            // Expiration warning if < 24h
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
        .background(colorScheme == .dark ? Color(white: 0.12) : Color(white: 0.95))
        .orbitalCard()
    }
}

// MARK: - Video Card
struct VideoCard: View {
    let video: Video
    let showingSteps: Bool
    @Environment(\.colorScheme) var colorScheme
    
    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            // Play button
            Image(systemName: "play.fill")
                .font(.caption)
                .foregroundStyle(OrbitalColors.accent)
                .frame(width: 24, height: 24)
                .padding(.top, 4)
            
            VStack(alignment: .leading, spacing: 8) {
                Text(video.problem)
                    .font(.subheadline)
                    .fontWeight(.medium)
                    .lineLimit(2)
                
                HStack {
                    Text(video.category)
                        .font(.caption)
                        .foregroundStyle(OrbitalColors.accent)
                    
                    Text("•")
                        .foregroundStyle(colorScheme == .dark ? OrbitalColors.textSecondaryDark : OrbitalColors.textSecondaryLight)
                    
                    Text(video.subcategory)
                        .font(.caption)
                        .foregroundStyle(colorScheme == .dark ? OrbitalColors.textSecondaryDark : OrbitalColors.textSecondaryLight)
                    
                    Spacer()
                    
                    Text(video.durationFormatted)
                        .font(.caption)
                        .foregroundStyle(colorScheme == .dark ? OrbitalColors.textSecondaryDark : OrbitalColors.textSecondaryLight)
                }
                
                if showingSteps {
                    // Show step preview
                    VStack(alignment: .leading, spacing: 2) {
                        ForEach(Array(video.stepPreview.prefix(2).enumerated()), id: \.offset) { index, step in
                            Text("\(index + 1). \(step)")
                                .font(.caption2)
                                .foregroundStyle(colorScheme == .dark ? OrbitalColors.textSecondaryDark : OrbitalColors.textSecondaryLight)
                        }
                        
                        if let result = video.result {
                            Text("Result: \(result)")
                                .font(.caption2)
                                .fontWeight(.medium)
                        }
                    }
                    .padding(.top, 4)
                }
            }
        }
        .padding()
        .orbitalCard()
    }
}

// MARK: - Empty State
struct EmptyStateView: View {
    @Environment(\.colorScheme) var colorScheme
    
    var body: some View {
        VStack(spacing: 16) {
            Image(systemName: "play.rectangle.on.rectangle")
                .font(.system(size: 48))
                .foregroundStyle(colorScheme == .dark ? OrbitalColors.textSecondaryDark : OrbitalColors.textSecondaryLight)
            
            Text("No videos yet")
                .font(.headline)
            
            Text("Solve your first problem to see it here")
                .font(.subheadline)
                .foregroundStyle(colorScheme == .dark ? OrbitalColors.textSecondaryDark : OrbitalColors.textSecondaryLight)
        }
    }
}

#Preview {
    LibraryView()
        .preferredColorScheme(.dark)
}
