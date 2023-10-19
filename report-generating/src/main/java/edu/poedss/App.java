package edu.poedss;

import org.camunda.bpm.client.ExternalTaskClient;
import org.camunda.bpm.engine.variable.Variables;
import org.camunda.bpm.engine.variable.value.ObjectValue;

import java.util.Collections;
import java.util.Random;

public class App 
{
    public static void main( String[] args )
    {
        ExternalTaskClient client = ExternalTaskClient.create()
        .baseUrl("http://camunda.local:8080/engine-rest")
        .build();

        // subscribe to the topic
        client.subscribe("generateReport")
        .lockDuration(1000)
        .handler((externalTask, externalTaskService) -> {

            // retrieve a variable from the Process Engine
            String patientId = externalTask.getVariable("patientId");


            String report = "Hello I am a report of patient " + patientId;

            // create an object typed variable
            ObjectValue reportObject = Variables
            .objectValue(report)
            .create();

            // complete the external task
            externalTaskService.complete(externalTask,
            Collections.singletonMap("report", reportObject));

            System.out.println("Generated report of process instance: " + externalTask.getId() + " has been completed!");

        }).open();

        // subscribe to the topic
        client.subscribe("logReport")
        .lockDuration(1000)
        .handler((externalTask, externalTaskService) -> {
            Boolean isReportConcern = externalTask.getVariable("CriticalReport");

            // create an object typed variable
            ObjectValue isReportConcernObject = Variables
            .objectValue(isReportConcern)
            .create();

            // complete the external task
            externalTaskService.complete(externalTask,
            Collections.singletonMap("isReportConcern", isReportConcernObject));

            System.out.println("Report has been evaluated in process instance:  " + externalTask.getId() + "!");

        }).open();
        }
}
