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

    let cellSpacingHeight: CGFloat = 15
    
    
    var apiURL = "https://api.unsplash.com/photos/random?client_id=jZIYt--FtgynjvcmEHVcbHEbViKIogcA_KY4wzhE-7Y"
    
    var clientThread: ClientThread!
    
    @IBOutlet weak var backView: UIView!
    @IBOutlet weak var tableview: UITableView!
    @IBOutlet weak var image: UIImageView!

    
    override func viewDidLoad() {
        loadBackgroundPhoto()
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        setUpElements()
        loadSampleDoors()
        setupTableView()
    }
    
    func setUpElements(){
        backView.backgroundColor = Colors.yellow
        backView.layer.cornerRadius = 50.0
        backView.layer.shouldRasterize = true
        
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
            
            let imageRandom = URL(string: yeyo.substring(with: first..<second))
            
            
            do {
                let data = try Data(contentsOf: imageRandom!)
                self.image.image = UIImage(data: data)
                print("Funciona?")
            } catch _ {
                print("Error")
            }
                
        }
    }
    
    private func loadSampleDoors() {
        imagenes.append(UIImage(named: "logo.png")!)
        self.allDevices = self.clientThread.getAllDevices()
    }
    
    func setClientThread(clientThread: ClientThread){
        self.clientThread = clientThread
    }

    
    func setupTableView() {
        tableview.delegate = self
        tableview.dataSource = self
    }
    
    func numberOfSections(in tableView: UITableView) -> Int {
        return self.allDevices.count
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return 1

    }
    
    func tableView(_ tableView: UITableView, viewForHeaderInSection section: Int) -> UIView? {
        let headerView = UIView()
        headerView.backgroundColor = UIColor.clear
        return headerView
    }
    
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 90
    }
    
    // Set the spacing between sections
    func tableView(_ tableView: UITableView, heightForHeaderInSection section: Int) -> CGFloat {
        return cellSpacingHeight
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
       
        let cell = Bundle.main.loadNibNamed("DoorEjTableViewCell", owner: self, options: nil)?.first as! DoorEjTableViewCell
        
        self.tableview.backgroundColor = Colors.yellow
        
        cell.heightAnchor.constraint(equalToConstant: 90).isActive = true
        cell.contentView.backgroundColor = Colors.yellow
        cell.viewEsta.layer.cornerRadius = cell.viewEsta.bounds.height / 2
        
        
        if self.allDevices[indexPath.section].getState() == 1 {
            cell.viewEsta.backgroundColor = Colors.open
        } else {
            cell.viewEsta.backgroundColor = UIColor.white
        }
        
        cell.mainImageView.image = self.allDevices[indexPath.section].getImage()
        cell.mainImageView.layer.cornerRadius = cell.mainImageView.bounds.height / 2
        cell.mainImageView.backgroundColor = UIColor.gray
        
        cell.mainLabek.text = self.allDevices[indexPath.section].getIdentifierName()
 
        return cell
    }
    
    func refresh(){
        DispatchQueue.main.async { [unowned self] in
            self.tableview.reloadData()
        }
    }
    
    
    // method to run when table view cell is tapped
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        // note that indexPath.section is used rather than indexPath.row
        if self.allDevices[indexPath.section].getState() == 1 {
            self.clientThread.sendCloseDevice(id_device: self.allDevices[indexPath.section].getID())
            //self.allDevices[indexPath.section].setState(state: "0")
        } else {
            self.clientThread.sendOpenDevice(id_device: self.allDevices[indexPath.section].getID())
            //self.allDevices[indexPath.section].setState(state: "1")
        }
        
        self.tableview.reloadData()
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
