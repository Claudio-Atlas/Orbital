import SwiftUI

struct ProfileView: View {
    @Environment(\.colorScheme) var colorScheme
    @EnvironmentObject var authManager: AuthManager
    @AppStorage("isDarkMode") private var isDarkMode = true
    @State private var showingPurchaseSheet = false
    @State private var showingSignOutAlert = false
    
    var body: some View {
        NavigationStack {
            List {
                // Account Section
                Section {
                    HStack {
                        // Avatar
                        Circle()
                            .fill(OrbitalColors.accent.opacity(0.2))
                            .frame(width: 60, height: 60)
                            .overlay(
                                Text(authManager.userEmail.prefix(1).uppercased())
                                    .font(.title2)
                                    .fontWeight(.bold)
                                    .foregroundStyle(OrbitalColors.accent)
                            )
                        
                        VStack(alignment: .leading, spacing: 4) {
                            Text(authManager.userEmail)
                                .font(.headline)
                            Text("Member since \(authManager.memberSince)")
                                .font(.caption)
                                .foregroundStyle(colorScheme == .dark ? OrbitalColors.textSecondaryDark : OrbitalColors.textSecondaryLight)
                        }
                    }
                    .padding(.vertical, 8)
                }
                
                // Balance Section
                Section("Balance") {
                    HStack {
                        VStack(alignment: .leading, spacing: 4) {
                            Text("\(authManager.minutesBalance, specifier: "%.1f") minutes")
                                .font(.title2)
                                .fontWeight(.bold)
                            Text("remaining")
                                .font(.caption)
                                .foregroundStyle(colorScheme == .dark ? OrbitalColors.textSecondaryDark : OrbitalColors.textSecondaryLight)
                        }
                        
                        Spacer()
                        
                        Button(action: { showingPurchaseSheet = true }) {
                            HStack {
                                Image(systemName: "plus")
                                Text("Buy More")
                            }
                            .font(.subheadline)
                            .fontWeight(.semibold)
                            .padding(.horizontal, 16)
                            .padding(.vertical, 10)
                            .background(OrbitalColors.accent)
                            .foregroundStyle(.white)
                            .clipShape(Capsule())
                        }
                    }
                    .padding(.vertical, 8)
                }
                
                // Preferences Section
                Section("Preferences") {
                    Toggle(isOn: $isDarkMode) {
                        Label("Dark Mode", systemImage: isDarkMode ? "moon.fill" : "sun.max.fill")
                    }
                    .tint(OrbitalColors.accent)
                    
                    NavigationLink {
                        Text("Voice Settings") // TODO: Implement
                    } label: {
                        Label("Default Voice", systemImage: "waveform")
                    }
                    
                    NavigationLink {
                        Text("Notifications") // TODO: Implement
                    } label: {
                        Label("Notifications", systemImage: "bell")
                    }
                }
                
                // History Section
                Section("History") {
                    NavigationLink {
                        PurchaseHistoryView()
                    } label: {
                        Label("Purchase History", systemImage: "creditcard")
                    }
                    
                    NavigationLink {
                        Text("Usage Stats") // TODO: Implement
                    } label: {
                        Label("Usage Stats", systemImage: "chart.bar")
                    }
                }
                
                // Support Section
                Section("Support") {
                    Link(destination: URL(string: "https://orbitalsolver.io/help")!) {
                        Label("Help Center", systemImage: "questionmark.circle")
                    }
                    
                    Link(destination: URL(string: "mailto:support@orbitalsolver.io")!) {
                        Label("Contact Support", systemImage: "envelope")
                    }
                    
                    NavigationLink {
                        Text("Terms of Service") // TODO: Link to web
                    } label: {
                        Label("Terms of Service", systemImage: "doc.text")
                    }
                    
                    NavigationLink {
                        Text("Privacy Policy") // TODO: Link to web
                    } label: {
                        Label("Privacy Policy", systemImage: "hand.raised")
                    }
                }
                
                // Sign Out
                Section {
                    Button(role: .destructive, action: { showingSignOutAlert = true }) {
                        Label("Sign Out", systemImage: "rectangle.portrait.and.arrow.right")
                    }
                }
                
                // App Info
                Section {
                    HStack {
                        Text("Version")
                        Spacer()
                        Text("1.0.0")
                            .foregroundStyle(colorScheme == .dark ? OrbitalColors.textSecondaryDark : OrbitalColors.textSecondaryLight)
                    }
                }
            }
            .navigationTitle("Profile")
            .alert("Sign Out", isPresented: $showingSignOutAlert) {
                Button("Cancel", role: .cancel) { }
                Button("Sign Out", role: .destructive) {
                    authManager.signOut()
                }
            } message: {
                Text("Are you sure you want to sign out?")
            }
            .sheet(isPresented: $showingPurchaseSheet) {
                PurchaseSheet()
            }
        }
    }
}

// MARK: - Purchase Sheet
struct PurchaseSheet: View {
    @Environment(\.dismiss) var dismiss
    @Environment(\.colorScheme) var colorScheme
    @State private var selectedTier: PricingTier = .standard
    
    var body: some View {
        NavigationStack {
            VStack(spacing: 24) {
                Text("Buy Minutes")
                    .font(.title2)
                    .fontWeight(.bold)
                
                Text("Choose a pack to start creating videos")
                    .font(.subheadline)
                    .foregroundStyle(colorScheme == .dark ? OrbitalColors.textSecondaryDark : OrbitalColors.textSecondaryLight)
                
                // Pricing tiers
                VStack(spacing: 12) {
                    ForEach(PricingTier.allCases) { tier in
                        PricingTierCard(tier: tier, isSelected: selectedTier == tier) {
                            selectedTier = tier
                        }
                    }
                }
                .padding(.horizontal)
                
                // Purchase button
                Button(action: purchaseMinutes) {
                    Text("Purchase \(selectedTier.minutes) minutes — $\(selectedTier.price, specifier: "%.2f")")
                        .fontWeight(.semibold)
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(OrbitalColors.accent)
                        .foregroundStyle(.white)
                        .clipShape(RoundedRectangle(cornerRadius: 12))
                }
                .padding(.horizontal)
                
                Spacer()
            }
            .padding(.top, 24)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button("Done") { dismiss() }
                }
            }
        }
        .presentationDetents([.medium, .large])
    }
    
    func purchaseMinutes() {
        // TODO: Implement Stripe checkout
        dismiss()
    }
}

// MARK: - Pricing Tier Card
struct PricingTierCard: View {
    let tier: PricingTier
    let isSelected: Bool
    let action: () -> Void
    @Environment(\.colorScheme) var colorScheme
    
    var body: some View {
        Button(action: action) {
            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    HStack {
                        Text(tier.name)
                            .font(.headline)
                        
                        if tier == .standard {
                            Text("Best Value")
                                .font(.caption2)
                                .fontWeight(.semibold)
                                .padding(.horizontal, 8)
                                .padding(.vertical, 4)
                                .background(OrbitalColors.accent)
                                .foregroundStyle(.white)
                                .clipShape(Capsule())
                        }
                    }
                    
                    Text("\(tier.minutes) minutes")
                        .font(.subheadline)
                        .foregroundStyle(colorScheme == .dark ? OrbitalColors.textSecondaryDark : OrbitalColors.textSecondaryLight)
                }
                
                Spacer()
                
                VStack(alignment: .trailing) {
                    Text("$\(tier.price, specifier: "%.2f")")
                        .font(.title3)
                        .fontWeight(.bold)
                    
                    Text("$\(tier.pricePerMinute, specifier: "%.2f")/min")
                        .font(.caption)
                        .foregroundStyle(colorScheme == .dark ? OrbitalColors.textSecondaryDark : OrbitalColors.textSecondaryLight)
                }
            }
            .padding()
            .background(isSelected ? OrbitalColors.accent.opacity(0.1) : (colorScheme == .dark ? OrbitalColors.cardDark : OrbitalColors.cardLight))
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(isSelected ? OrbitalColors.accent : (colorScheme == .dark ? OrbitalColors.cardBorderDark : OrbitalColors.cardBorderLight), lineWidth: isSelected ? 2 : 1)
            )
            .clipShape(RoundedRectangle(cornerRadius: 12))
        }
        .buttonStyle(.plain)
    }
}

// MARK: - Purchase History View
struct PurchaseHistoryView: View {
    var body: some View {
        List {
            Text("Purchase history will appear here")
                .foregroundStyle(.secondary)
        }
        .navigationTitle("Purchase History")
    }
}

#Preview {
    ProfileView()
        .environmentObject(AuthManager())
        .preferredColorScheme(.dark)
}
