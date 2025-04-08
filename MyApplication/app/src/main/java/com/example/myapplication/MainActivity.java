/////sol kol uzatma

package com.example.myapplication;

import android.os.Bundle;

import com.aldebaran.qi.sdk.QiContext;
import com.aldebaran.qi.sdk.QiSDK;
import com.aldebaran.qi.sdk.RobotLifecycleCallbacks;
import com.aldebaran.qi.sdk.builder.AnimateBuilder;
import com.aldebaran.qi.sdk.builder.AnimationBuilder;
import com.aldebaran.qi.sdk.builder.SayBuilder;
import com.aldebaran.qi.sdk.design.activity.RobotActivity;
import com.aldebaran.qi.sdk.object.actuation.Animate;
import com.aldebaran.qi.sdk.object.actuation.Animation;
import com.aldebaran.qi.sdk.object.conversation.Say;

public class MainActivity extends RobotActivity implements RobotLifecycleCallbacks {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        QiSDK.register(this, this);
    }

    @Override
    protected void onDestroy() {
        QiSDK.unregister(this, this);
        super.onDestroy();
    }

    @Override
    public void onRobotFocusGained(QiContext qiContext) {
        // Konuşma
        Say say = SayBuilder.with(qiContext)
                .withText("Şimdi sol kolumu uzatıyorum.")
                .build();
        say.run();

        // Animasyonu çalıştır
        Animation animation = AnimationBuilder.with(qiContext)
                .withResources(R.raw.pointfrontl) // dosya adı küçük harflerle ve uzantısız
                .build();

        Animate animate = AnimateBuilder.with(qiContext)
                .withAnimation(animation)
                .build();

        animate.run();
    }

    @Override
    public void onRobotFocusLost() {
        // Odak kaybedilirse
    }

    @Override
    public void onRobotFocusRefused(String reason) {
        // Odak alınamazsa
    }
}