package com.example.root.upfiletransfer;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.os.Environment;
import android.support.v7.app.AppCompatActivity;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.View;
import android.widget.Button;
import android.widget.HorizontalScrollView;
import android.widget.ListView;
import android.widget.TextView;

import java.io.File;
import java.util.ArrayList;

public class DisplayFilesActivity extends AppCompatActivity {
    ListView lvFiles;
    TextView tvFolderEmpty, tvCurrentFolder;
    HorizontalScrollView hsvFolderScroll;
    Button bSend, bCancel;

    public String username ;

    FileListAdapter fileListAdapter;
    String currentDirectoryPath;

    ArrayList<File> filesToBeSentSet;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_display_files);

        lvFiles = (ListView) findViewById(R.id.lvFiles);
        tvFolderEmpty = (TextView) findViewById(R.id.tvFolderEmpty);
        tvCurrentFolder = (TextView) findViewById(R.id.tvCurrentFolder);
        hsvFolderScroll = (HorizontalScrollView) findViewById(R.id.hsvFolderScroll);
        bSend = (Button) findViewById(R.id.bSend);
        bCancel = (Button) findViewById(R.id.bCancel);

        currentDirectoryPath = Environment.getExternalStorageDirectory().getAbsolutePath();
        fileListAdapter = new FileListAdapter(this, R.layout.file_list_item, getVisibleFiles(currentDirectoryPath));
        lvFiles.setAdapter(fileListAdapter);
        tvCurrentFolder.setText(currentDirectoryPath);


        username = getIntent().getStringExtra("username");
        // make tvCurrentFolder scroll to end whenever folder changes
        tvCurrentFolder.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence charSequence, int i, int i1, int i2) {

            }

            @Override
            public void onTextChanged(CharSequence charSequence, int i, int i1, int i2) {
                hsvFolderScroll.post(new Runnable() {
                    @Override
                    public void run() {
                        hsvFolderScroll.fullScroll(HorizontalScrollView.FOCUS_RIGHT);
                    }
                });
            }

            @Override
            public void afterTextChanged(Editable editable) {

            }
        });

        filesToBeSentSet = new ArrayList<>();

        bSend.setEnabled(false);
        bSend.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(DisplayFilesActivity.this, PeerChooserActivity.class);
                intent.putExtra("filesToBeSent", filesToBeSentSet);
                intent.putExtra("username" , username );
                startActivity(intent);
            }
        });
        bCancel.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                finish();
            }
        });
    }

    public File[] getVisibleFiles(String directoryPath) {
        File[] files = new File(directoryPath).listFiles();
        int visibleFileCount = 0;
        for (File f: files) {
            if (!f.isHidden()) {
                ++visibleFileCount;
            }
        }
        if (visibleFileCount == 0) {
            tvFolderEmpty.setVisibility(View.VISIBLE);
        } else {
            tvFolderEmpty.setVisibility(View.INVISIBLE);
        }
        File[] retFiles = new File[visibleFileCount];
        for (int i = 0, j = 0; i < files.length; ++i) {
            if (!files[i].isHidden()) {
                retFiles[j++] = files[i];
            }
        }
        return retFiles;
    }

    @Override
    public void onBackPressed() {
        if (currentDirectoryPath.equals(Environment.getExternalStorageDirectory().getAbsolutePath())) {
            if (filesToBeSentSet.size() > 0) {
                System.out.println(filesToBeSentSet.size());
                new AlertDialog.Builder(DisplayFilesActivity.this)
                        .setTitle("Cancel")
                        .setMessage("Are you sure want to cancel sending the selected files?")
                        .setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialogInterface, int i) {
                                DisplayFilesActivity.super.onBackPressed();
                            }
                        })
                        .setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialogInterface, int i) {
                            }
                        })
                        .setIcon(R.drawable.ic_error)
                        .show();
            } else {
                super.onBackPressed();
            }
        } else {
            fileListAdapter.files = getVisibleFiles(currentDirectoryPath.substring(0, currentDirectoryPath.lastIndexOf('/')));
            currentDirectoryPath = currentDirectoryPath.substring(0, currentDirectoryPath.lastIndexOf('/'));
            fileListAdapter.notifyDataSetChanged();
            tvCurrentFolder.setText(currentDirectoryPath);
        }
    }

    @Override
    public boolean onSupportNavigateUp() {
        onBackPressed();
        return true;
    }
}
