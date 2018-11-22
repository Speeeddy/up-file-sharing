package com.example.root.upfiletransfer;

public class HistoryList {

    private String name ;
    private String filename ;
    private String timestamp ;
    private String action ;


    public void setName(String s){
        this.name = s ;
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
    public String getName(){
        return name ;
    }
    public String getFilename(){
        return filename ;
    }
    public String getAction(){
        return action ;
    }

    @Override
    public String toString() {
        return "\nSender/Receiver : " + getName() + "\n" + "Filename : " + getFilename() + "\n" + "Time : " + getTimestamp() + "\n" + "Action : " + getAction() + "\n";
    }
}
