//
//  Device.swift
//  prueba5
//
//  Created by Alejandro Nieto Alarcon on 12/05/2020.
//  Copyright © 2020 Alejandro Nieto Alarcon. All rights reserved.
//

import Foundation

class Device {
    
    var id: Int?
    var identifier_name: String?
    var state: Int?
    var maintenance: Int?
    var image = [UInt8]()

    init(id: String, identifier_name: String, state: String, maintenance: String) {
        self.id = Int(id)
        self.identifier_name = identifier_name
        self.state = Int(state)
        self.maintenance = Int(maintenance)
    }
    
    func setImage(image: [UInt8]){
        self.image = image
    }
    
    func setState(state: String){
        self.state = Int(state)
    }
    
    func getID() -> Int {
        return self.id!
    }
    
    func getIdentifierName() -> String {
        return self.identifier_name!
    }
    
    func getState() -> Int {
        return self.state!
    }
    
    func getImage() -> [UInt8] {
        return self.image
    }
}
