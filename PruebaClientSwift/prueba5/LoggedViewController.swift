//
//  LoggedViewController.swift
//  prueba5
//
//  Created by Alejandro Nieto Alarcon on 30/03/2020.
//  Copyright © 2020 Alejandro Nieto Alarcon. All rights reserved.
//

import UIKit

class LoggedViewController: UIViewController, UITableViewDelegate,  UITableViewDataSource  {

    var puertas = [String]()

    var inputStream: InputStream!
    var outputStream: OutputStream!
    
    
    @IBOutlet weak var tableview: UITableView!
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
       
        loadSampleDoors()
        setupTableView()
    }
    
    private func loadSampleDoors() {
        //let door1 = Door()
        var door1 = "puerta1"
        var door2 = "puerta2"
        var door3 = "puerta3"
        
        puertas +=  [door1, door2, door3]
        
        print("Que es esto -->" , puertas.count)
        
        
    }
    
    func setInputStream(inputStream: InputStream){
        self.inputStream = inputStream
    }
    
    func setOutputStream(outputStream: OutputStream){
        self.outputStream = outputStream
    }
    
    func setupTableView() {
        tableview.delegate = self
        tableview.dataSource = self
        tableview.register(DoorTableViewCell.self, forCellReuseIdentifier: "Door")
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        // 1
        return puertas.count
    }
    
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 100
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
       
        let cell = tableview.dequeueReusableCell(withIdentifier: "Door", for: indexPath) as! DoorTableViewCell
        
        cell.message = puertas[indexPath.row]
        
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
