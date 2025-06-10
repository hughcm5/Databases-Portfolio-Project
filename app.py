# All code is based on the CS340 starter code unless stated otherwise
# Citation for app.py: 
# Date: 12/10/23
# Based on app.py from:
# https://github.com/osu-cs340-ecampus/flask-starter-app 

from flask import Flask, render_template, json, redirect, request
from flask_mysqldb import MySQL
import os
import db_connector as db

#------DB CONFIG------
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_user'
app.config['MYSQL_PASSWORD'] = 'XXXX' 
app.config['MYSQL_DB'] = 'cs340_user'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

#------CRUD FUNCTIONS-------
# All of our CRUD functions make use of the functions:
# execute_query() and connect_to_database() from @mlapresta's
# db_connector.py from the CS340 starter code
# Citation for the execute_query and connect_to_database functions:
# Date: 12/10/23
# Copied from db_connector.py from: 
# https://github.com/osu-cs340-ecampus/flask-starter-app 
# orginated from: https://github.com/mlapresta/cs340_starter_app


@app.route('/')
def root():
    return render_template('index.html')


# Citation for the allowed_jobs CRUD functions: 
# Date: 12/10/23
# adapted from:
# https://github.com/osu-cs340-ecampus/flask-starter-app
# modified using flask's features for requesting data, redirections, and variable rules
# from: https://flask.palletsprojects.com/en/3.0.x/quickstart/#accessing-request-data

# allowed jobs
# create and read allowed jobs
@app.route('/AllowedJobs', methods=['GET', 'POST'])
def allowed_jobs():
    # create db connection
    db_connection = db.connect_to_database()

    # create job
    if request.method == 'POST':
        jobName = request.form['jobName']
        jobID = request.form['jobID']
        query = "INSERT INTO AllowedJobs (jobName, jobID) VALUES (%s, %s)"
        db.execute_query(db_connection, query, (jobName, jobID))

    # read jobs
    query = "SELECT * FROM AllowedJobs"
    allowed_jobs_data = db.execute_query(db_connection, query).fetchall()
    return render_template('allowedjobs.html', allowed_jobs=allowed_jobs_data)

# update job
@app.route('/update_job/<string:jobName>', methods=['GET', 'POST'])
def update_job(jobName):
    # create db connection
    db_connection = db.connect_to_database()

    #update job
    if request.method == 'POST':
        newJobID = request.form['jobID']
        newJobName = request.form['jobName']
        query = "UPDATE AllowedJobs SET jobID = %s, jobName = %s WHERE jobName = %s"
        db.execute_query(db_connection, query, (newJobID, newJobName, jobName))
        return redirect('/AllowedJobs')

    # read jobs
    query = "SELECT * FROM AllowedJobs WHERE jobName = %s"
    job_data = db.execute_query(db_connection, query, (jobName,)).fetchone()
    return render_template('update_job.html', job=job_data)

# delete job
@app.route('/delete_job/<string:jobName>', methods=['POST'])
def delete_job(jobName):
    # create db connection
    db_connection = db.connect_to_database()
    
    # delete job
    query = "DELETE FROM AllowedJobs WHERE jobName = %s"
    db.execute_query(db_connection, query, (jobName,))
    return redirect('/AllowedJobs')

#---------------------
# Citation for the allowed_ranks CRUD functions: 
# Date: 12/10/23
# adapted from:
# https://github.com/osu-cs340-ecampus/flask-starter-app
# modified using flask's features for requesting data, redirections, and variable rules
# from: https://flask.palletsprojects.com/en/3.0.x/quickstart/#accessing-request-data

# allowed ranks routes
# create and read ranks
@app.route('/AllowedRanks', methods=['GET', 'POST'])
def allowed_ranks():
    # create db connection
    db_connection = db.connect_to_database()
    
    # create rank
    if request.method == 'POST':
        rankName = request.form['rankName']
        rankID = request.form['rankID']
        query = "INSERT INTO AllowedRanks (rankName, rankID) VALUES (%s, %s)"
        db.execute_query(db_connection, query, (rankName, rankID))

    # read ranks
    query = "SELECT * FROM AllowedRanks"
    allowed_ranks_data = db.execute_query(db_connection, query).fetchall()
    return render_template('allowedranks.html', allowed_ranks=allowed_ranks_data)

# update rank
@app.route('/update_rank/<string:rankName>', methods=['GET', 'POST'])
def update_rank(rankName):
    # create db connection
    db_connection = db.connect_to_database()
    
    # update rank
    if request.method == 'POST':
        newRankID = request.form['rankID']
        newRankName = request.form['rankName']
        query = "UPDATE AllowedRanks SET rankName = %s, rankID = %s WHERE rankName = %s"
        db.execute_query(db_connection, query, (newRankName, newRankID, rankName))
        return redirect('/AllowedRanks')

    # read rank
    query = "SELECT * FROM AllowedRanks WHERE rankName = %s"
    rank_data = db.execute_query(db_connection, query, (rankName,)).fetchone()
    return render_template('update_rank.html', rank=rank_data)

# delete rank
@app.route('/delete_rank/<string:rankName>', methods=['POST'])
def delete_rank(rankName):
    # create db connection
    db_connection = db.connect_to_database()
    
    # delete rank
    query = "DELETE FROM AllowedRanks WHERE rankName = %s"
    db.execute_query(db_connection, query, (rankName,))
    return redirect('/AllowedRanks')

#---------------------
# Citation for the inventories CRUD functions: 
# Date: 12/10/23
# adapted from:
# https://github.com/osu-cs340-ecampus/flask-starter-app
# modified using flask's features for requesting data, redirections, and variable rules
# from: https://flask.palletsprojects.com/en/3.0.x/quickstart/#accessing-request-data

# inventories routes
# create and read inventories
@app.route('/Inventories', methods=['GET', 'POST'])
def inventories():
    # create db connection
    db_connection = db.connect_to_database()
    
    # create inventory
    if request.method == 'POST':
        equipmentOwned = request.form['equipmentOwned']
        creditBalance = request.form['creditBalance']
        query = "INSERT INTO Inventories (equipmentOwned, creditBalance) VALUES (%s, %s)"
        db.execute_query(db_connection, query, (equipmentOwned, creditBalance))

    # read inventory
    query = "SELECT * FROM Inventories"
    cursor = db.execute_query(db_connection, query)
    inventories_data = cursor.fetchall()
    return render_template('inventories.html', inventories=inventories_data)

# update inventory
@app.route('/update_inventory/<int:inventoryID>', methods=['GET', 'POST'])
def update_inventory(inventoryID):
    # create db connection
    db_connection = db.connect_to_database()
    
    # update inventory
    if request.method == 'POST':
        equipmentOwned = request.form['equipmentOwned']
        creditBalance = request.form['creditBalance']
        query = "UPDATE Inventories SET equipmentOwned = %s, creditBalance = %s WHERE inventoryID = %s"
        db.execute_query(db_connection, query, (equipmentOwned, creditBalance, inventoryID))
        return redirect('/Inventories')

    # read inventory
    query = "SELECT * FROM Inventories WHERE inventoryID = %s"
    cursor = db.execute_query(db_connection, query, (inventoryID,))
    inventory_data = cursor.fetchone()
    return render_template('update_inventory.html', inventory=inventory_data)

# delete inventories
@app.route('/delete_inventory/<int:inventoryID>', methods=['POST'])
def delete_inventory(inventoryID):
    # create db connection
    db_connection = db.connect_to_database()
    
    # delete inventory
    query = "DELETE FROM Inventories WHERE inventoryID = %s"
    db.execute_query(db_connection, query, (inventoryID,))
    return redirect('/Inventories')

#----------------
# Citation for the equipment CRUD functions: 
# Date: 12/10/23
# adapted from:
# https://github.com/osu-cs340-ecampus/flask-starter-app
# modified using flask's features for requesting data, redirections, and variable rules
# from: https://flask.palletsprojects.com/en/3.0.x/quickstart/#accessing-request-data

# equipment routes
# create and read equipment
@app.route('/Equipment', methods=['GET', 'POST'])
def equipment():
    # create db connection
    db_connection = db.connect_to_database()
    
    # create equipment
    if request.method == 'POST':
        equipmentType = request.form['equipmentType']
        creditCost = request.form['creditCost']
        equipmentName = request.form['equipmentName']
        query = "INSERT INTO Equipment (equipmentType, creditCost, equipmentName) VALUES (%s, %s, %s)"
        db.execute_query(db_connection, query, (equipmentType, creditCost, equipmentName))

    # read equipment
    query = "SELECT * FROM Equipment"
    cursor = db.execute_query(db_connection, query)
    equipment_data = cursor.fetchall()
    return render_template('equipment.html', equipment=equipment_data)

# update equipment
@app.route('/update_equipment/<int:equipmentID>', methods=['GET', 'POST'])
def update_equipment(equipmentID):
    # create db connection
    db_connection = db.connect_to_database()
    
    # update equipment
    if request.method == 'POST':
        equipmentType = request.form['equipmentType']
        equipmentName = request.form['equipmentName'] 
        creditCost = request.form['creditCost']
        query = "UPDATE Equipment SET equipmentType = %s, equipmentName = %s, creditCost = %s WHERE equipmentID = %s"
        db.execute_query(db_connection, query, (equipmentType, equipmentName, creditCost, equipmentID))
        return redirect('/Equipment')

    # read equipment
    query = "SELECT * FROM Equipment WHERE equipmentID = %s"
    cursor = db.execute_query(db_connection, query, (equipmentID,))
    equipment_data = cursor.fetchone()
    return render_template('update_equipment.html', equipment=equipment_data)

# delete equipment
@app.route('/delete_equipment/<int:equipmentID>', methods=['POST'])
def delete_equipment(equipmentID):
    # create db connection
    db_connection = db.connect_to_database()
    
    # delete equipment
    query = "DELETE FROM Equipment WHERE equipmentID = %s"
    db.execute_query(db_connection, query, (equipmentID,))
    return redirect('/Equipment')

#-------------------
# Citation for the missions CRUD functions: 
# Date: 12/10/23
# adapted from:
# https://github.com/osu-cs340-ecampus/flask-starter-app
# modified using flask's features for requesting data, redirections, and variable rules
# from: https://flask.palletsprojects.com/en/3.0.x/quickstart/#accessing-request-data

# missions routes
# create and read missions
@app.route('/Missions', methods=['GET', 'POST'])
def missions():
    # create db connection
    db_connection = db.connect_to_database()
    
    # create mission
    if request.method == 'POST':
        missionType = request.form['missionType']
        creditReward = request.form['creditReward']
        resourceID = request.form.get('resourceID')
        query = "INSERT INTO Missions (missionType, creditReward, resourceID) VALUES (%s, %s, %s)"
        db.execute_query(db_connection, query, (missionType, creditReward, resourceID))

    # read missions
    query = "SELECT * FROM Missions"
    missions_data = db.execute_query(db_connection, query).fetchall()
    return render_template('missions.html', missions=missions_data)

# update missions
@app.route('/update_mission/<int:missionID>', methods=['GET', 'POST'])
def update_mission(missionID):
    # create db connection
    db_connection = db.connect_to_database()
    
    # update mission
    if request.method == 'POST':
        missionType = request.form['missionType']
        creditReward = request.form['creditReward']
        resourceID = request.form.get('resourceID')
        query = "UPDATE Missions SET missionType = %s, creditReward = %s, resourceID = %s WHERE missionID = %s"
        db.execute_query(db_connection, query, (missionType, creditReward, resourceID, missionID))
        return redirect('/Missions')

    # read mission
    query = "SELECT * FROM Missions WHERE missionID = %s"
    mission_data = db.execute_query(db_connection, query, (missionID,)).fetchone()
    return render_template('update_mission.html', mission=mission_data)

# delete mission
@app.route('/delete_mission/<int:missionID>', methods=['POST'])
def delete_mission(missionID):
    # create db connection
    db_connection = db.connect_to_database()      

    # delete mission
    query = "DELETE FROM Missions WHERE missionID = %s"
    db.execute_query(db_connection, query, (missionID,))
    return redirect('/Missions')

#--------------------
# Citation for the miners CRUD functions: 
# Date: 12/10/23
# adapted from:
# https://github.com/osu-cs340-ecampus/flask-starter-app
# modified using flask's features for requesting data, redirections, and variable rules
# from: https://flask.palletsprojects.com/en/3.0.x/quickstart/#accessing-request-data

# create and read miners
@app.route('/Miners', methods=['GET', 'POST'])
def miners():
    # create db connection
    db_connection = db.connect_to_database()
    
    # create miner
    if request.method == 'POST':
        jobName = request.form['jobName']
        rankName = request.form['rankName']
        inventoryID = request.form.get('inventoryID')
        activeMission = request.form.get('activeMission')
        query = "INSERT INTO Miners (jobName, rankName, inventoryID, activeMission) VALUES (%s, %s, %s, %s)"
        db.execute_query(db_connection, query, (jobName, rankName, inventoryID, activeMission))

    # read miners
    query = "SELECT * FROM Miners"
    miners_data = db.execute_query(db_connection, query).fetchall()
    return render_template('miners.html', miners=miners_data)

# update miners
@app.route('/update_miner/<int:minerID>', methods=['GET', 'POST'])
def update_miner(minerID):
    # create db connection
    db_connection = db.connect_to_database()
    
    # update miner
    if request.method == 'POST':
        jobName = request.form['jobName']
        rankName = request.form['rankName']
        inventoryID = request.form.get('inventoryID')
        activeMission = request.form.get('activeMission')
        query = "UPDATE Miners SET jobName = %s, rankName = %s, inventoryID = %s, activeMission = %s WHERE minerID = %s"
        db.execute_query(db_connection, query, (jobName, rankName, inventoryID, activeMission, minerID))
        return redirect('/Miners')

    # read miner
    query = "SELECT * FROM Miners WHERE minerID = %s"
    miner_data = db.execute_query(db_connection, query, (minerID,)).fetchone()
    return render_template('update_miner.html', miner=miner_data)

# delete miner
@app.route('/delete_miner/<int:minerID>', methods=['POST'])
def delete_miner(minerID):
    # create db connection
    db_connection = db.connect_to_database()
    
    # delete miner
    query = "DELETE FROM Miners WHERE minerID = %s"
    db.execute_query(db_connection, query, (minerID,))
    return redirect('/Miners')

#-------------
# Citation for the resources CRUD functions: 
# Date: 12/10/23
# adapted from:
# https://github.com/osu-cs340-ecampus/flask-starter-app
# modified using flask's features for requesting data, redirections, and variable rules
# from: https://flask.palletsprojects.com/en/3.0.x/quickstart/#accessing-request-data

# create and read resources
@app.route('/Resources', methods=['GET', 'POST'])
def resources():
    # create db connection
    db_connection = db.connect_to_database()
    
    # create resource
    if request.method == 'POST':
        resourceName = request.form['resourceName']
        resourceValue = request.form['resourceValue']
        query = "INSERT INTO Resources (resourceName, resourceValue) VALUES (%s, %s)"
        db.execute_query(db_connection, query, (resourceName, resourceValue))

    # read resources
    query = "SELECT * FROM Resources"
    resources_data = db.execute_query(db_connection, query).fetchall()
    return render_template('resources.html', resources=resources_data)

# update resource
@app.route('/update_resource/<int:resourceID>', methods=['GET', 'POST'])
def update_resource(resourceID):
    # create db connection
    db_connection = db.connect_to_database()
    
    # update resource
    if request.method == 'POST':
        resourceName = request.form['resourceName']
        resourceValue = request.form['resourceValue']
        query = "UPDATE Resources SET resourceName = %s, resourceValue = %s WHERE resourceID = %s"
        db.execute_query(db_connection, query, (resourceName, resourceValue, resourceID))
        return redirect('/Resources')

    # read resources
    query = "SELECT * FROM Resources WHERE resourceID = %s"
    resource_data = db.execute_query(db_connection, query, (resourceID,)).fetchone()
    return render_template('update_resource.html', resource=resource_data)

# delete resources
@app.route('/delete_resource/<int:resourceID>', methods=['POST'])
def delete_resource(resourceID):
    # create db connection
    db_connection = db.connect_to_database()
    
    # delete resource
    query = "DELETE FROM Resources WHERE resourceID = %s"
    db.execute_query(db_connection, query, (resourceID,))
    return redirect('/Resources')

# Intersection Table
# Citation for the ResourceTotal CRUD functions: 
# Date: 12/10/23
# adapted from:
# https://github.com/osu-cs340-ecampus/flask-starter-app
# modified using flask's features for requesting data, redirections, and variable rules
# from: https://flask.palletsprojects.com/en/3.0.x/quickstart/#accessing-request-data

@app.route("/ResourceTotal", methods=['GET', 'POST'])
def resource_total():
    # create db connection
    db_connection = db.connect_to_database()
    
    # create resourcetotal
    if request.method == 'POST':
        resourceID = request.form.get('resourceID')
        missionID = request.form.get('missionID')
        query = 'INSERT INTO ResourceTotal (resourceID, missionID) VALUES (%s, %s)'
        db.execute_query(db_connection, query, (resourceID, missionID))

        # read resourcetotal
        query = '''
        SELECT rt.resourceTotalID, rt.resourceID, r.resourceValue, rt.missionID, m.creditReward
        FROM `ResourceTotal` rt
        JOIN Resources r ON rt.resourceID = r.resourceID
        JOIN Missions m ON rt.missionID = m.missionID
        ORDER BY resourceTotalID
        '''
        resources_data = db.execute_query(db_connection, query) 
        return render_template('resourcetotal.html', data=resources_data)

    if request.method == 'GET':
        query = '''
        SELECT rt.resourceTotalID, rt.resourceID, r.resourceValue, rt.missionID, m.creditReward
        FROM `ResourceTotal` rt
        JOIN Resources r ON rt.resourceID = r.resourceID
        JOIN Missions m ON rt.missionID = m.missionID
        ORDER BY resourceTotalID
        '''
        resources_data = db.execute_query(db_connection, query).fetchall()
        return render_template('resourcetotal.html', data=resources_data)


# Delete resource total
@app.route('/delete_resourcetotal/<int:resourceTotalID>', methods=['POST'])
def delete_resourcetotal(resourceTotalID):
    # create db connection
    db_connection = db.connect_to_database()
    
    # delete resource
    query = "DELETE FROM ResourceTotal WHERE resourceTotalID = %s"
    db.execute_query(db_connection, query, (resourceTotalID,))
    return redirect('/ResourceTotal')

# update resource
@app.route('/update_resource_total/<int:resourceTotalID>', methods=['GET', 'POST'])
def update_resource_total(resourceTotalID):
    # create db connection
    db_connection = db.connect_to_database()    

    # update resource
    if request.method == 'POST':
        resourceID = request.form.get('resourceID')
        resourceValue = request.form.get('resourceValue')
        missionID = request.form.get('missionID')
        creditReward = request.form.get('creditReward')
        query = "UPDATE ResourceTotal SET resourceID = %s, resourceValue = %s, missionID = %s, creditReward = %s WHERE resourceTotalID = %s"
        db.execute_query(db_connection, query, (resourceID, resourceValue, missionID, creditReward, resourceTotalID))
        return redirect('/ResourceTotal')

    # read resources
    query = "SELECT * FROM ResourceTotal WHERE resourceTotalID = %s"
    resource_data = db.execute_query(db_connection, query, (resourceTotalID,)).fetchone()
    return render_template('update_resource_total.html', resourcetotal=resource_data)

# Inventories Has Equipment
@app.route("/InventoriesHasEquipment", methods=['GET', 'POST'])
def inventories_has_equipment():
    # create db connection
    db_connection = db.connect_to_database()
    if not db_connection:
        return "error"

    # create resourcetotal
    if request.method == 'POST':
        equipmentID = request.form.get('equipmentID')
        inventoryID = request.form.get('inventoryID')
        query = 'INSERT INTO InventoriesHasEquipment (equipmentID, inventoryID) VALUES (%s, %s)'
        db.execute_query(db_connection, query, (equipmentID, inventoryID))

        # read resourcetotal
        query = '''
            SELECT e.equipmentID, i.inventoryID
            FROM `InventoriesHasEquipment`
            JOIN Equipment e ON InventoriesHasEquipment.equipmentID = e.equipmentID
            JOIN Inventories i ON InventoriesHasEquipment.inventoryID = i.inventoryID
            ORDER BY e.equipmentID
            '''

        resources_data = db.execute_query(db_connection, query) 
        return render_template('inventorieshasequipment.html', data=resources_data)

    if request.method == 'GET':
        query = '''
        SELECT e.equipmentID, i.inventoryID
        FROM `InventoriesHasEquipment`
        JOIN Equipment e ON InventoriesHasEquipment.equipmentID = e.equipmentID
        JOIN Inventories i ON InventoriesHasEquipment.inventoryID = i.inventoryID
        ORDER BY equipmentID
        '''
        resources_data = db.execute_query(db_connection, query).fetchall()
        return render_template('inventorieshasequipment.html', data=resources_data)
    
# Delete resource total
@app.route('/delete_inventories_has_equipment/<int:equipmentID>', methods=['POST'])
def delete_inventories_has_equipment(equipmentID):
    # create db connection
    db_connection = db.connect_to_database()
    if not db_connection:
        return "error"

    # delete resource
    query = "DELETE FROM InventoriesHasEquipment WHERE equipmentID = %s"
    db.execute_query(db_connection, query, (equipmentID,))
    return redirect('/InventoriesHasEquipment')

# update inventories has equipment
@app.route('/update_inventories_has_equipment/<int:equipmentID>', methods=['GET', 'POST'])
def update_inventories_has_equipment(equipmentID):
    # create db connection
    db_connection = db.connect_to_database()
    if not db_connection:
        return "error"

    # update resource
    if request.method == 'POST':
        equipmentID = request.form.get('equipmentID')
        inventoryID = request.form.get('inventoryID')
        query = "UPDATE InventoriesHasEquipment SET equipmentID = %s, inventoryID = %s WHERE equipmentID = %s"
        db.execute_query(db_connection, query, (equipmentID, inventoryID))
        return redirect('/InventoriesHasEquipment')

    # read resources
    query = "SELECT * FROM InventoriesHasEquipment WHERE equipmentID = %s"
    inventory_has_data = db.execute_query(db_connection, query, (equipmentID,)).fetchone()
    return render_template('update_inventories_has_equipment.html', equipment_inventories=inventory_has_data)




# select port
if __name__ == "__main__":
    app.run(port=55900, debug=True)