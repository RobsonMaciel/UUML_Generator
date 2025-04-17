// UIManager.h
#pragma once

#include "CoreMinimal.h"
#include "UIManager.generated.h"

UCLASS()
class YOURPROJECT_API AUIManager {
    GENERATED_BODY()

public:
    AUIManager();

    UFUNCTION(BlueprintCallable, Category = "UI")
    void ShowMainMenu();

    UFUNCTION(BlueprintCallable, Category = "UI")
    void ShowInventory();

    UFUNCTION(BlueprintCallable, Category = "UI")
    void ShowQuestLog();

    UFUNCTION(BlueprintCallable, Category = "UI")
    void UpdateHealthBar(int health);

    UFUNCTION(BlueprintCallable, Category = "UI")
    void UpdateStaminaBar(int stamina);
}
