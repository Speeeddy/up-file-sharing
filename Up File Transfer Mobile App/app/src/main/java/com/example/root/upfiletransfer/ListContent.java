package com.example.root.upfiletransfer;

public class ListContent {
    private String name ;
    private String filename ;
    private String timestamp ;
    private String size ;

    public int compareTo(ListContent other) {
        return timestamp.compareTo(other.timestamp);
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
    public void setName(String s){
        this.name = s ;
    }
    public void setFilename(String s){
        this.filename = s ;
    }
    public void setTimestamp(String s){
        this.timestamp = s ;
    }
    public String getSize(){
        return size ;
    }
    public void setSize(String s){
        this.size = s ;
    }

    @Override
    public String toString() {

        float mb = Float.parseFloat(getSize());
        mb = mb / (1024*1024);
        String lol = String.format("%.2f" , mb);
        
        return "\nSender : " + getName() + "\n" + "Filename : " + getFilename() + "\n" + getTimestamp() + "\n"
                + "Size : " + lol + " MB" + "\n";

    }
}
