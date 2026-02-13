import Foundation

enum PricingTier: String, CaseIterable, Identifiable {
    case starter
    case standard
    case pro
    
    var id: String { rawValue }
    
    var name: String {
        switch self {
        case .starter: return "Starter"
        case .standard: return "Standard"
        case .pro: return "Pro"
        }
    }
    
    var minutes: Int {
        switch self {
        case .starter: return 10
        case .standard: return 50
        case .pro: return 120
        }
    }
    
    var price: Double {
        switch self {
        case .starter: return 2.00
        case .standard: return 8.00
        case .pro: return 15.00
        }
    }
    
    var pricePerMinute: Double {
        price / Double(minutes)
    }
    
    var stripePriceId: String {
        switch self {
        case .starter: return "price_starter"
        case .standard: return "price_standard"
        case .pro: return "price_pro"
        }
    }
}
