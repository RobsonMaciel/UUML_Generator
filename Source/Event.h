// Event.h
#pragma once

#include "CoreMinimal.h"
#include "Event.generated.h"

UCLASS()
class YOURPROJECT_API AEvent {
    GENERATED_BODY()

public:
    AEvent();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Event")
    FString Name;

    UFUNCTION(BlueprintCallable, Category = "Event")
    void Trigger();

    UFUNCTION(BlueprintCallable, Category = "Event")
    void Cancel();
}
