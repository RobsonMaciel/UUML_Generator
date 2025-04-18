// PlayerCharacter.h
#pragma once

#include "CoreMinimal.h"
#include "Character.h"
#include "PlayerCharacter.generated.h"

UCLASS()
class YOURPROJECT_API APlayerCharacter : public ACharacter {
    GENERATED_BODY()

public:
    APlayerCharacter();

    UFUNCTION(BlueprintCallable, Category = "Game")
    void SaveGame();

    UFUNCTION(BlueprintCallable, Category = "Game")
    void LoadGame();

    UFUNCTION(BlueprintCallable, Category = "Equipment")
    void EquipArmor(class AArmor* armor);

    UFUNCTION(BlueprintCallable, Category = "Equipment")
    void UnequipArmor(class AArmor* armor);

    UFUNCTION(BlueprintCallable, Category = "Customization")
    void CustomizeAppearance();
}
