const express = require("express");
const app = express();
const router = express.Router();
const { createLogger, transports } = require("winston");

const logger = createLogger({transports:[new transports.Console]});

router.get("/user",function(req,res){

    try{

    } catch(err){
        logger.err("Routes","GET user", "Error : "+JSON.stringify(err));
    }
});

router.post("/user",function(req,res){
    try{

    } catch(err){
        logger.err("Routers","POST user", "Error : "+JSON.stringify(err));
    }
})