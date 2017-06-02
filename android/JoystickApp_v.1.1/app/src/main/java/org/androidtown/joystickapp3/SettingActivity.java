package org.androidtown.joystickapp3;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import java.net.Socket;

public class SettingActivity extends AppCompatActivity {

    // 에딧 텍스트, 버튼 객체 생성
    EditText editTextAddress, editTextPort;
    Button connectBtn, disConnectBtn;

    Socket socket = null;
    SocketInfo sock;


    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_setting);

        //앱 기본 스타일 설정
        getSupportActionBar().setElevation(0);

        connectBtn = (Button) findViewById(R.id.buttonConnect); // 연결 버튼
        disConnectBtn = (Button) findViewById(R.id.buttonClear); // 연결해체 버튼
        editTextAddress = (EditText) findViewById(R.id.addressText); // IP 주소 입력
        editTextPort = (EditText) findViewById(R.id.portText); // 포트번호 입력

        sock = SocketInfo.getInstance();

        //connect 버튼 클릭
        connectBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                String destAddr = editTextAddress.getText().toString(); // 입력된 IP 주소 불러옴
                int destPort = Integer.parseInt(editTextPort.getText().toString()); // 입력된 포트 번호 불러옴
                sock.setDestAddress(destAddr, destPort); // 서버 주소, 서버 포트 설정
                Log.d("debug","make socket try");

                // 연결 Toast Messsage
                Toast.makeText(getApplicationContext(), "Connection complete", Toast.LENGTH_SHORT).show();

            }
        });

        //disconnect 버튼 클릭
        disConnectBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                sock.disconnect(); // 소켓 연결 해제
                // 연결 해제 Toast Messsage
                Toast.makeText(getApplicationContext(), "Disconnection complete", Toast.LENGTH_SHORT).show();
            }
        });
    }

    // 설정 화면 창 닫기
    public void onCloseButtonClicked(View v) {
        finish();
    }

}


