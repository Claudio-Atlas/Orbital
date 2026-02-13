import SwiftUI

struct OrbitalLogo: View {
    var body: some View {
        Image("OrbitalLogo")
            .resizable()
            .aspectRatio(contentMode: .fit)
            // Soft purple glow behind logo - slightly stronger
            .shadow(color: OrbitalColors.accent.opacity(0.6), radius: 25, x: 0, y: 0)
            .shadow(color: OrbitalColors.accent.opacity(0.4), radius: 45, x: 0, y: 0)
            .shadow(color: OrbitalColors.accent.opacity(0.2), radius: 70, x: 0, y: 0)
    }
}

#Preview {
    OrbitalLogo()
        .frame(width: 150, height: 150)
        .padding()
        .background(Color.black)
}
