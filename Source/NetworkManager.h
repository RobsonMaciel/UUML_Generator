// NetworkManager.h
#pragma once

#include "CoreMinimal.h"
#include "NetworkManager.generated.h"

UCLASS()
class YOURPROJECT_API ANetworkManager {
    GENERATED_BODY()

public:
    ANetworkManager();

    UFUNCTION(BlueprintCallable, Category = "Network")
    void ConnectToServer(FString serverAddress);

    UFUNCTION(BlueprintCallable, Category = "Network")
    void Disconnect();

    UFUNCTION(BlueprintCallable, Category = "Network")
    void SendData(FString data);

    UFUNCTION(BlueprintCallable, Category = "Network")
    void ReceiveData();
}
