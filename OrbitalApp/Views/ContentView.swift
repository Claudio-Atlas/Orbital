//
//  ContentView.swift
//  Orbital - AI Math Video Solver
//
//  Root view that switches between login and main tab navigation
//  based on authentication state.
//
//  Copyright © 2026 Onyx Enterprises. All rights reserved.
//

import SwiftUI

/// Root content view that handles auth state routing.
/// Shows LoginView when logged out, MainTabView when authenticated.
struct ContentView: View {
    @EnvironmentObject var authManager: AuthManager
    @AppStorage("isDarkMode") private var isDarkMode = true
    @State private var selectedTab = 0
    
    var body: some View {
        Group {
            if authManager.isAuthenticated {
                MainTabView(selectedTab: $selectedTab)
            } else {
                LoginView()
            }
        }
        .preferredColorScheme(isDarkMode ? .dark : .light)
    }
}

struct MainTabView: View {
    @Binding var selectedTab: Int
    @EnvironmentObject var authManager: AuthManager
    @ObservedObject var accentTheme = AccentTheme.shared
    
    var body: some View {
        TabView(selection: $selectedTab) {
            SolverView()
                .tabItem {
                    Image(systemName: "sparkles.rectangle.stack")
                    Text("Solver")
                }
                .tag(0)
            
            LibraryView()
                .tabItem {
                    Image(systemName: "play.rectangle.on.rectangle")
                    Text("Solves")
                }
                .tag(1)
            
            ProfileView()
                .tabItem {
                    Image(systemName: "person.circle")
                    Text("Me")
                }
                .tag(2)
        }
        .tint(OrbitalColors.accent)
    }
}

#Preview {
    ContentView()
        .environmentObject(AuthManager())
}
