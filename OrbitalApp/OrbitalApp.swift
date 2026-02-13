//
//  OrbitalApp.swift
//  Orbital - AI Math Video Solver
//
//  Main app entry point. Handles global state injection and theme management.
//
//  Copyright © 2026 Onyx Enterprises. All rights reserved.
//

import SwiftUI

@main
struct OrbitalApp: App {
    @StateObject private var authManager = AuthManager()
    @AppStorage("isDarkMode") private var isDarkMode = true
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(authManager)
                .preferredColorScheme(isDarkMode ? .dark : .light)
        }
    }
}
