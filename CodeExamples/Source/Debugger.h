// Debugger.h
#pragma once

#include "CoreMinimal.h"
#include "Debugger.generated.h"

UCLASS()
class YOURPROJECT_API ADebugger {
    GENERATED_BODY()

public:
    ADebugger();

    UFUNCTION(BlueprintCallable, Category = "Debug")
    void Log(FString message);

    UFUNCTION(BlueprintCallable, Category = "Debug")
    void LogError(FString message);

    UFUNCTION(BlueprintCallable, Category = "Debug")
    void LogWarning(FString message);
}
