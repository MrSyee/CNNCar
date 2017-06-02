package org.androidtown.joystickapp3;

import android.content.Intent;
import android.graphics.drawable.ColorDrawable;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.CompoundButton;
import android.widget.SeekBar;
import android.widget.TextView;
import android.widget.ToggleButton;

import static org.androidtown.joystickapp3.R.id.seekBar;


public class MainActivity extends AppCompatActivity {

    private SeekBar seekbar1; // 속도바
    private SeekBar seekbar2; // 조향바
    private TextView text1; // 조향 값
    private TextView text2; // 속도 값
    private ToggleButton toggle2; // 전진 or 후진

    private int stearing = 50; // 조향
    private int accel = 0; // 속도
    private int direction = 0; // 방향


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        direction = 1; // 전진 (defalut)
        SendMessage.start(); // 쓰레드 시작

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        //액션바 설정하기//
        //액션바 타이틀 변경하기
        getSupportActionBar().setTitle("Joystick Module");
        //액션바 배경색 변경
        getSupportActionBar().setBackgroundDrawable(new ColorDrawable(0xFF3F51B5));
        //홈버튼 표시
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);


        seekbar1 = (SeekBar) findViewById(seekBar); // 속도 바
        seekbar2 = (SeekBar) findViewById(R.id.seekBar2); // 조향 바
        text2 = (TextView) findViewById(R.id.textView2); // 속도 값 표시
        text1 = (TextView) findViewById(R.id.textView); // 조향 값 표시
        toggle2 = (ToggleButton) findViewById(R.id.toggleButton2);  // 전진 or후진

        //조향 seekbar 설정
        seekbar2.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener()
        {
            //thumb가 멈출 때 호출
            public void onStopTrackingTouch(SeekBar seekBar)
            {
                seekBar.setProgress(50); // 버튼을 뗄 때마다 조향을 중앙으로 조정
            }

            //thumb가 움직이기 시작할 때 호출
            public void onStartTrackingTouch(SeekBar seekBar)
            {}

            //thumb 가 움직일때 마다 호출
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser)
            {
                stearing = progress; // stearing 변수에 seekbar의 값을 저장
                text1.setText(Integer.toString(progress)); //좌측 text창에 조향 값 표시
            }
        });

        //속도 seekbar 설정
        seekbar1.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener()
        {
            //thumb가 멈출 때 호출
            public void onStopTrackingTouch(SeekBar seekBar)
            {
                text2.setText(Integer.toString(seekBar.getProgress())); // 우측 text창에 속도 값 표시
            }

            //thumb가 움직이기 시작할 때 호출
            public void onStartTrackingTouch(SeekBar seekBar)
            {}

            //thumb 가 움직일때 마다 호출
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser)
            {
                accel = progress; // accel 변수에 seekbar의 값을 저장
                text2.setText(Integer.toString(progress)); // 우측 text창에 속도 값 표시
            }
        });


        toggle2.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                // 역방향
                if (isChecked == true) {
                    direction = -1;
                }
                // 정방향
                else{
                    direction = 1;
                }
            }
        });
    }


    // 액션버튼 메뉴 액션바에 집어 넣기
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu, menu);
        return true;
    }

    // 액션버튼을 클릭했을때의 동작
    @Override
    public boolean onOptionsItemSelected(MenuItem item){
        int id = item.getItemId();

        // menu select
        if (id == android.R.id.home) {
            finish();
            return true;
        }

        // 서버 연결 설정 창 열기
        if (id == R.id.action_setting) {
            Intent intent = new Intent(this, SettingActivity.class);
            startActivity(intent);
            return true;
        }

        return super.onOptionsItemSelected(item);
    }


    // Remote Controller 쓰레드
    private Thread SendMessage = new Thread() {
        public void run() {
            int former_accel = 0;
            int former_stearing = 0;
            int former_direction = 0;
            String myMessage = "";
            SocketInfo sock = SocketInfo.getInstance();
            try {
                while (true) {
                    sleep(150);
                    if(!sock.connected()) continue;

                    // 속도, 조향, 방향 값이 바뀌는 경우에만 메시지 전송
                    if(former_accel != accel || former_stearing != stearing || former_direction != direction){
                        myMessage = Integer.toString(direction * accel) + " " + Integer.toString(stearing);
                        sock.sendMessage(myMessage);
                        former_accel = accel;
                        former_stearing = stearing;
                        former_direction = direction;
                    }
                }
            } catch (Exception e) {

            }
        }
    };
}






