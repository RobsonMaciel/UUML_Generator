// System.h
#pragma once

#include "CoreMinimal.h"
#include "System.generated.h"

UCLASS()
class YOURPROJECT_API ASystem {
    GENERATED_BODY()

public:
    ASystem();

    UFUNCTION(BlueprintCallable, Category = "System")
    void Restart();

    UFUNCTION(BlueprintCallable, Category = "System")
    void Shutdown();
}
