// WebSocket.h
#pragma once

#include "CoreMinimal.h"
#include "WebSocket.generated.h"

UCLASS()
class YOURPROJECT_API AWebSocket {
    GENERATED_BODY()

public:
    AWebSocket();

    UFUNCTION(BlueprintCallable, Category = "Network")
    void Connect(FString url);

    UFUNCTION(BlueprintCallable, Category = "Network")
    void Send(FString message);

    UFUNCTION(BlueprintCallable, Category = "Network")
    void Receive();
}
