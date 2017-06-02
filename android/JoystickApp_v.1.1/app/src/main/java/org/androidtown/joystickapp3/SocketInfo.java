package org.androidtown.joystickapp3;

import android.os.AsyncTask;
import java.io.IOException;
import java.io.OutputStream;
import java.net.Socket;
import static android.os.SystemClock.sleep;


// 싱글톤 패턴
public class SocketInfo {

    String dstAddress; // IP 주소
    int dstPort; // 포트 번호
    Socket dstSocket; // 소켓

    private static SocketInfo sock = new SocketInfo();
    public static SocketInfo getInstance() {
        return sock;
    }
    private SocketInfo(){
        // 소켓정보 초기값
        dstAddress = "";
        dstPort = -1;
        dstSocket = null;
    }

    // 서버 포트 설정
    public void setDestAddress(String d,int p){
        this.dstAddress = d;
        this.dstPort = p;

        // 연결 확인 메시지
        sendMessage("0 100");
        sleep(150);
        sendMessage("0 50");
        sleep(150);
    }

    // 연결 해제
    public boolean connected(){
        if(dstSocket != null)
            return true;
        else return false;
    }
    public void disconnect(){
        sendMessage("-1 -1");
        sleep(300);

        this.dstAddress = "";
        this.dstPort = -1;
        this.dstSocket = null;
    }

    // 서버로 메시지 전송
    public void sendMessage(String d){
        SocketAsync send = new SocketAsync(d);
        send.execute();
        send = null;
    }

    // 메시지 전송 (비동기 작업)
    public class SocketAsync  extends AsyncTask<Void, Void, Void>{
        String sendMessage;
        public SocketAsync(String message) {
            this.sendMessage = message;
        }

        protected Void doInBackground(Void... arg0) {
            try {
                // IP 주소 또는 포트 설정이 안 된 경우 메시지전송 안함
                if (dstAddress == "" || dstPort == -1) return null;

                // 소켓 생성
                else if (dstSocket == null) dstSocket = new Socket(dstAddress, dstPort);

                OutputStream out = dstSocket.getOutputStream();
                out.write(sendMessage.getBytes());
            } catch (IOException e) {
                // do nothing
            }
            return null;
        }
    }
}
