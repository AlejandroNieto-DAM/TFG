//
//  LoggedViewController.swift
//  prueba5
//
//  Created by Alejandro Nieto Alarcon on 30/03/2020.
//  Copyright © 2020 Alejandro Nieto Alarcon. All rights reserved.
//

import UIKit
import Alamofire

class LoggedViewController: UIViewController, UITableViewDelegate,  UITableViewDataSource  {

    var puertas = [String]()
    var imagenes = [UIImage]()

    var inputStream: InputStream!
    var outputStream: OutputStream!
    
    var allDevices = [Device]()

    
    @IBOutlet weak var image: UIImageView!
    
    var apiURL = "https://api.unsplash.com/photos/random?client_id=jZIYt--FtgynjvcmEHVcbHEbViKIogcA_KY4wzhE-7Y"
    
    
    @IBOutlet weak var tableview: UITableView!
    
    override func viewDidLoad() {
        loadBackgroundPhoto()
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        
        loadSampleDoors()
        setupTableView()
    }
    
    private func loadBackgroundPhoto(){
        // 1
        let request = AF.request(apiURL)
        // 2
        request.responseJSON { (data) in
            //print(data)
            let yeyo = data.description
            
            var first = 0
            var second = 0

            let index = yeyo.range(of: "regular = ")?.lowerBound
            let distance = yeyo.distance(from: yeyo.startIndex, to: index!)
            first = distance + 11
            
            let index2 = yeyo.range(of: "small = ")?.lowerBound
            let distance2 = yeyo.distance(from: index!, to: index2!)
            second = first + distance2
            second = second - 22
            
            print(yeyo.substring(with: first..<second))
            
            let imageRandom = URL(fileURLWithPath: yeyo.substring(with: first..<second))
            
            self.image.load(url: imageRandom)
            //self.image.backgroundColor = Colors.firstBlue
    
        }
    }
    
    private func loadSampleDoors() {
        imagenes.append(UIImage(named: "logo.png")!)
    }
    
    func setAllDevices(allDevices: [Device]){
        self.allDevices = allDevices
    }

    
    func setupTableView() {
        tableview.delegate = self
        tableview.dataSource = self
    }
    
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        // 1
        return allDevices.count
    }
    
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 90
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
       
        let cell = Bundle.main.loadNibNamed("DoorEjTableViewCell", owner: self, options: nil)?.first as! DoorEjTableViewCell
        cell.heightAnchor.constraint(equalToConstant: 90).isActive = true
        
        cell.viewEsta.layer.cornerRadius = cell.viewEsta.bounds.height / 2
        cell.viewEsta.backgroundColor = Colors.firstBlue
        cell.mainImageView.image = imagenes[0]
        cell.mainImageView.layer.cornerRadius = cell.mainImageView.bounds.height / 2
        cell.mainImageView.backgroundColor = UIColor.gray
        cell.mainLabek.text = self.allDevices[indexPath.row].getIdentifierName()
 
        print("Hey!")
        
        return cell
    }
    
    
    
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}

extension UIImageView {
    func load(url: URL) {
        DispatchQueue.global().async { [weak self] in
            if let data = try? Data(contentsOf: url) {
                if let image = UIImage(data: data) {
                    DispatchQueue.main.async {
                        self?.image = image
                    }
                }
            }
        }
    }
}

extension String {
    func index(from: Int) -> Index {
        return self.index(startIndex, offsetBy: from)
    }

    func substring(from: Int) -> String {
        let fromIndex = index(from: from)
        return String(self[fromIndex...])
    }

    func substring(to: Int) -> String {
        let toIndex = index(from: to)
        return String(self[..<toIndex])
    }

    func substring(with r: Range<Int>) -> String {
        let startIndex = index(from: r.lowerBound)
        let endIndex = index(from: r.upperBound)
        return String(self[startIndex..<endIndex])
    }
}
