// Feedback.h
#pragma once

#include "CoreMinimal.h"
#include "Feedback.generated.h"

UCLASS()
class YOURPROJECT_API AFeedback {
    GENERATED_BODY()

public:
    AFeedback();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Feedback")
    FString Message;

    UFUNCTION(BlueprintCallable, Category = "Feedback")
    void SendFeedback();

    UFUNCTION(BlueprintCallable, Category = "Feedback")
    void ReceiveFeedback();
}
