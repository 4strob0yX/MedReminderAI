package com.medreminder.ai

import android.app.Application
import com.medreminder.ai.di.AppContainer

class MedReminderApp : Application() {
    lateinit var container: AppContainer

    override fun onCreate() {
        super.onCreate()
        container = AppContainer(this)
    }
}
