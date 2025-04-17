// Localization.h
#pragma once

#include "CoreMinimal.h"
#include "Localization.generated.h"

UCLASS()
class YOURPROJECT_API ALocalization {
    GENERATED_BODY()

public:
    ALocalization();

    UFUNCTION(BlueprintCallable, Category = "Localization")
    FString GetLocalizedString(FString key);

    UFUNCTION(BlueprintCallable, Category = "Localization")
    void SetLanguage(FString language);
}
