// EventManager.h
#pragma once

#include "CoreMinimal.h"
#include "EventManager.generated.h"

UCLASS()
class YOURPROJECT_API AEventManager {
    GENERATED_BODY()

public:
    AEventManager();

    UFUNCTION(BlueprintCallable, Category = "Events")
    void TriggerEvent(FString eventName);

    UFUNCTION(BlueprintCallable, Category = "Events")
    void Subscribe(FString eventName, void method());

    UFUNCTION(BlueprintCallable, Category = "Events")
    void Unsubscribe(FString eventName, void method());
}
