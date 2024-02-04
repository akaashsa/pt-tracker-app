const express = require("express");
const app = express();
const router = express.Router();
const { createLogger, transports } = require("winston");

const logger = createLogger({transports:[new transports.Console]});

router.get("/exercise",function(req,res){

    try{

    } catch(err){
        logger.err("Routes","GET exercise", "Error : "+JSON.stringify(err));
    }
});

router.post("/exercise",function(req,res){
    try{

    } catch(err){
        logger.err("Routers","POST exercise", "Error : "+JSON.stringify(err));
    }
})