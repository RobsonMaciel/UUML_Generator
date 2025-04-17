// NPC.h
#pragma once

#include "CoreMinimal.h"
#include "Character.h"
#include "NPC.generated.h"

UCLASS()
class YOURPROJECT_API ANPC : public ACharacter {
    GENERATED_BODY()

public:
    ANPC();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Dialogue")
    FString Dialogue;

    UFUNCTION(BlueprintCallable, Category = "Interaction")
    void Speak();

    UFUNCTION(BlueprintCallable, Category = "AI")
    void FollowPlayer(APlayerCharacter* player);

    UFUNCTION(BlueprintCallable, Category = "Quests")
    void GiveQuest(class AQuest* quest);

    UFUNCTION(BlueprintCallable, Category = "Quests")
    void CompleteQuest(class AQuest* quest);
}
