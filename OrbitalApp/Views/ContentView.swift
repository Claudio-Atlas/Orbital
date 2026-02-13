import SwiftUI

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
