//
//  PricingTier.swift
//  Orbital - AI Math Video Solver
//
//  Pricing tier definitions matching Stripe products.
//  Used for display purposes in the app; actual checkout happens on web.
//
//  Tiers:
//    - Starter: $2 for 10 minutes ($0.20/min)
//    - Standard: $8 for 50 minutes ($0.16/min)
//    - Pro: $15 for 120 minutes ($0.125/min)
//
//  Copyright © 2026 Onyx Enterprises. All rights reserved.
//

import Foundation

/// Pricing tier definitions for minute packages.
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
