// WebRequest.h
#pragma once

#include "CoreMinimal.h"
#include "WebRequest.generated.h"

UCLASS()
class YOURPROJECT_API AWebRequest {
    GENERATED_BODY()

public:
    AWebRequest();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Network")
    FString URL;

    UFUNCTION(BlueprintCallable, Category = "Network")
    void Send();

    UFUNCTION(BlueprintCallable, Category = "Network")
    void Receive();
}
