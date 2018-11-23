package com.example.root.upfiletransfer;

public class HistoryList {

    private String sender ;
    private String receiver ;
    private String filename ;
    private String timestamp ;
    private String action ;


    public void setSender(String s){
        this.sender = s ;
    }
    public void setReceiver(String s){
        this.receiver = s ;
    }
    public void setFilename(String s){
        this.filename = s ;
    }
    public void setTimestamp(String s){
        this.timestamp = s ;
    }
    public void setAction(String s){
        this.action = s ;
    }

    public String getTimestamp(){
        return timestamp ;
    }
    public String getReceiver(){
        return receiver ;
    }
    public String getFilename(){
        return filename ;
    }
    public String getAction(){
        return action ;
    }
    public String getSender(){return sender;}

    @Override
    public String toString() {
        return "\nSender : " + getSender() + "\n" + "Receiver : " + getReceiver() + "\n" + "Filename : " + getFilename() + "\n" + "Time : " + getTimestamp() + "\n" + "Action : " + getAction() + "\n";
    }
}
