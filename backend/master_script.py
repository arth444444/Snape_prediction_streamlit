import Script_fetch_from_db
import Parse
import process
import dataprocess
import laggeddata
import weatherunion_script
import model_predict
import app

def main():
    Script_fetch_from_db.run()
    Parse.run()
    process.run()
    dataprocess.run()
    laggeddata.run()
    weatherunion_script.run()
    model_predict.run()
    app.run()
    

if __name__ == "__main__":
    main()






