// ScriptableObject.h
#pragma once

#include "CoreMinimal.h"
#include "ScriptableObject.generated.h"

UCLASS()
class YOURPROJECT_API UScriptableObject : public UObject {
    GENERATED_BODY()

public:
    UScriptableObject();

    UFUNCTION(BlueprintCallable, Category = "Scriptable")
    void Initialize();

    UFUNCTION(BlueprintCallable, Category = "Scriptable")
    void Save();
}
