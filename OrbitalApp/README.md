# Orbital iOS App

SwiftUI app for the Orbital math video solver.

## Setup Instructions

### 1. Create Xcode Project

1. Open Xcode
2. File → New → Project
3. Choose **iOS → App**
4. Settings:
   - Product Name: **OrbitalApp**
   - Team: Your team
   - Organization Identifier: `io.orbitalsolver`
   - Interface: **SwiftUI**
   - Language: **Swift**
   - Storage: **None**
5. Save to `~/Desktop/Orbital/`

### 2. Copy Source Files

After creating the project, copy these folders into the project:

```
OrbitalApp/
├── OrbitalApp.swift          (replace the generated one)
├── Views/
│   ├── ContentView.swift
│   ├── SolverView.swift
│   ├── LibraryView.swift
│   ├── ProfileView.swift
│   └── LoginView.swift
├── Components/
│   └── OrbitalLogo.swift
├── Theme/
│   └── OrbitalColors.swift
├── Models/
│   ├── Video.swift
│   └── PricingTier.swift
└── Managers/
    └── AuthManager.swift
```

### 3. Add to Xcode

1. In Xcode, right-click the OrbitalApp folder in the navigator
2. "Add Files to OrbitalApp..."
3. Select all the folders/files
4. Make sure "Copy items if needed" is checked
5. Click Add

### 4. Build & Run

1. Select an iPhone simulator (iPhone 15 Pro recommended)
2. Cmd+R to build and run

## Features

- ✅ Dark/Light theme support
- ✅ Solver input with example problems
- ✅ Video library with search
- ✅ Solution preview mode
- ✅ Profile & settings
- ✅ Purchase flow (UI only)
- ✅ Supabase authentication
- ✅ Token storage in Keychain (via @AppStorage)

## TODO

- [ ] Camera/photo upload
- [ ] Video player view
- [ ] Push notifications
- [ ] Stripe in-app purchase
- [ ] Google OAuth via ASWebAuthenticationSession
- [ ] Offline support

## API Configuration

The app connects to:
- Supabase: `https://pqwhfiuvcsjfevjwljml.supabase.co`
- API: `https://orbital-production-7c22.up.railway.app` (when ready)

## Screenshots

Based on mockups:
1. **Solver** - Enter problem, generate video
2. **Library** - Browse solved problems
3. **Profile** - Settings, purchase minutes
