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
