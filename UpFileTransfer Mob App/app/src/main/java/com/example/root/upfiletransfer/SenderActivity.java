package com.example.root.upfiletransfer;

import android.app.ProgressDialog;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ListView;
import android.widget.Toast;

import org.apache.commons.codec.binary.Base64;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;

public class SenderActivity extends AppCompatActivity {
    ListView lvStatus;
    Button bDone, bCancel;

    public String sender ;
    public String hue = "" ;
    public String receiver ;
    ArrayList<File> filesToBeSent;
//    ProgressDialog dialog;

    SenderFileListAdapter senderFileListAdapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sender);

        Toast.makeText(getApplicationContext() , "Sending Files. Please Wait." , Toast.LENGTH_LONG).show();

        lvStatus = (ListView) findViewById(R.id.lvStatus);
        bDone = (Button) findViewById(R.id.bDone);
//        bCancel = (Button) findViewById(R.id.bCancel);

        sender = getIntent().getStringExtra("sender") ;
        receiver = getIntent().getStringExtra("receiver") ;

        bDone.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(SenderActivity.this, SendReceive.class);
                intent.putExtra("username" , sender) ;
                intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
                startActivity(intent);
            }
        });
//        bCancel.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View view) {
//                finish();
//            }
//        });

        filesToBeSent = (ArrayList<File>) getIntent().getSerializableExtra("filesToBeSent");
        System.out.println(filesToBeSent);

        senderFileListAdapter = new SenderFileListAdapter(getApplicationContext(), R.layout.sender_file_progress_list_item, filesToBeSent);
        lvStatus.setAdapter(senderFileListAdapter);

        for(File f : filesToBeSent) {

//            String encode = null ;
//            try {
//                byte[] bytes = loadFile(f);
//                encode = new String(Base64.encodeBase64(bytes));
//
//                Log.d("Encode : ", encode);
//
////                        encode = "HELLO" ;
//                JSONObject jsonObject = new JSONObject();
//
//                jsonObject.put("name", sender);
//                jsonObject.put("sendto", receiver);
//                jsonObject.put("filename", f.getName());
//                jsonObject.put("data", encode);
//                hue = jsonObject.toString(1);
//            } catch (JSONException e) {
//                e.printStackTrace();
//            } catch (IOException e) {
//                e.printStackTrace();
//            }
//            dialog = ProgressDialog.show(SenderActivity.this, "",
//                    "Uploading. Please wait...", true);
            new SenderAsyncTask(SenderActivity.this, getIntent().getStringExtra("sender"),
                    getIntent().getStringExtra("receiver"))
                    .execute(f);
        }


//        dialog.dismiss();

//        Intent intent = new Intent(SenderActivity.this, SendReceive.class);
//        intent.putExtra("username" , sender) ;
//        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
//        startActivity(intent);
//        bDone.setEnabled(true);
//        bCancel.setEnabled(true);
    }

    private static byte[] loadFile(File file) throws IOException {
        InputStream is = new FileInputStream(file);

        long length = file.length();
        if (length > Integer.MAX_VALUE) {
            // File is too large
        }
        byte[] bytes = new byte[(int)length];

        int offset = 0;
        int numRead = 0;
        while (offset < bytes.length
                && (numRead=is.read(bytes, offset, bytes.length-offset)) >= 0) {
            offset += numRead;
        }

        if (offset < bytes.length) {
            throw new IOException("Could not completely read file "+file.getName());
        }

        is.close();
        return bytes;
    }
}
