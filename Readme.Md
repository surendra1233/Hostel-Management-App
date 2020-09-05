## Hostel Management App

A Social media app to manage different groups for different hostels.


### Setup

**To Run:**

Install required packages

```shell
conda env create -f flask_app.yml
```

From the current Directory 
run the following

```shell
export FLASK_APP=app/main_app.py
flask run
```

### ADMIN ACCESS FOR A GROUP 

    User must be present the group.
    run th following in terminal after starting the app
```shell
    db.session.query(memb).filter(memb.c.user_id == User.query.filter_by(username= <your_username> )[0].id).update({"status" : memb.c.status + 2}synchronize_session=False)
```
    