// ScriptingManager.h
#pragma once

#include "CoreMinimal.h"
#include "ScriptingManager.generated.h"

UCLASS()
class YOURPROJECT_API AScriptingManager {
    GENERATED_BODY()

public:
    AScriptingManager();

    UFUNCTION(BlueprintCallable, Category = "Scripting")
    void ExecuteScript(FString scriptName);

    UFUNCTION(BlueprintCallable, Category = "Scripting")
    void LoadScript(FString scriptName);
}
